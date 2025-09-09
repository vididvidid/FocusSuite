import cv2
import os
import tempfile
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
from skimage.metrics import structural_similarity as ssim
from moviepy.editor import VideoFileClip
import shutil

SSIM_THRESHOLD = 0.95

class VideoProcessor:
    def __init__(self, logger, progress_callback):
        self.logger = logger
        self.progress_callback = progress_callback

    def _extract_unique_frames (self, video_path):
        self.logger.info(f"Starting frame extraction for {video_path}")
        self.progress_callback("Step 1/4: Extracting unique frames...")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.logger.error("Could not open video file.")
            self.progress_callback("Error: Could not open video file.")
            return None, 0, 0

        unique_frames_data = []
        last_frame_gray = None
        frame_count =0
        saved_count =0

        temp_dir = tempfile.mkdtemp(prefix="focusvideo_")
        self.logger.info(f"Created temporary directory for frames: {temp_dir}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count +=1
            current_frame_small = cv2.resize(frame, (256, 144))
            current_frame_gray = cv2.cvtColor(current_frame_small, cv2.COLOR_BGR2GRAY)

            if last_frame_gray is not None:
                score, _ = ssim(last_frame_gray, current_frame_gray, full=True)
                if score > SSIM_THRESHOLD:
                    continue

            last_frame_gray = current_frame_gray
            frame_filename = os.path.join(temp_dir, f"frame_{saved_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            unique_frames_data.append({'original_index':frame_count - 1, 'path': frame_filename, 'blur': False})
            saved_count +=1

            if saved_count %10 == 0:
                self.progress_callback(f"Setup 1/4: Extracted {saved_count} unique frames from ~{frame_count}/{total_frames}...")

        cap.release()
        self.logger.info(f"Found {len(unique_frames_data)} unique frames out of {frame_count}.")
        self.progress_callback(f"Step 1/4: Found {len(unique_frames_data)} unique frames to analyze.")
        return unique_frames_data, fps, temp_dir

    def _process_frames_api(self, frames_to_process, prompt, api_manager):
        self.logger.info(f"Starting parallael API processing for {len(frames_to_process)} frames.")
        self.progress_callback("Step 2/4: Analyzing frames with AI (this may take a while)...")

        processed_count=0
        total_to_process = len(frames_to_process)
        lock = threading.Lock()

        def process_single_frame(frame_data):
            nonlocal processed_count
            full_prompt = f"""You are an automated image analysis system. Your sole function is to identify a specific object in an image and respond with a single word. 
**Task:** Determine if the image contains the following object: '{prompt}'
**Instructions:**
1. If the object is present, even partially, your entier response must be the exact word: yes
2. If the obejct is NOT present, or if you are uncertain, your entire response must be the exact word: no
3. Do NOT provide any explanation, punctuation, or any other text. 
"""
            response = api_manager.get_image_description(frame_data['path'], full_prompt)
            if response and 'yes' in response.lower():
                frame_data['blur'] = True

            with lock:
                processed_count+=1
                if processed_count % 5 ==0 or  processed_count == total_to_process:
                    self.progress_callback(f"Step 2/4: Analyzed {processed_count}/{total_to_process} frames...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_single_frame, frames_to_process)

        self.logger.info("Finished API processing.")
        self.progress_callback("Step 2/4: Frame analysis complete.")
        return frames_to_process

    def _reconstruct_video(self, original_video_path, processed_frames, fps, output_path, temp_dir):
        self.logger.info("Starting robus video reconstruction.")
        self.progress_callback("Step 3/4: Building blur timeiline...")

        cap = cv2.VideoCapture(original_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        blur_timeline = np.zeros(total_frames, dtype = bool)
        if processed_frames:
            sorted_frames = sorted(processed_frames, key=lambda x: x['original_index'])

            for i in range(len(sorted_frames)-1):
                start_info = sorted_frames[i]
                end_info = sorted_frames[i+1]
                start_index = start_info['original_index']
                end_index = end_info['original_index']
                blur_status = start_info['blur']
                blur_timeline[start_index: end_index] = blur_status

            last_frame_info = sorted_frames[-1]
            last_index = last_frame_info['original_index']
            last_blur_status = last_frame_info['blur']
            blur_timeline[last_index:] = last_blur_status


        self.progress_callback("Step 3/4: Rebuilding video from timeline...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = os.path.join(temp_dir, "temp_video_no_audio.mp4")
        out= cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

        frame_map = {frame['original_index']: frame for frame in processed_frames}
        last_unique_frame_image = None

        for i in range(total_frames):
            if i in frame_map:
                last_unique_frame_image = cv2.imread(frame_map[i]['path'])

            if last_unique_frame_image is not None:
                if blur_timeline[i]:
                    output_image = cv2.GaussianBlur(last_unique_frame_image, (251,251), 0)
                else:
                    output_image = last_unique_frame_image
                out.write(output_image)

            if i > 0 and i %100 == 0:
                self.progress_callback(f"Step 3/4: rebuild {i}/{total_frames} frames..")


        out.release()

        self.logger.info("Video frames rebuilt. Adding original audio...")
        self.progress_callback("Step 4/4: Finalizing video with audio...")

        original_clip = None
        video_clip = None
        final_clip = None

        try:
            original_clip = VideoFileClip(original_video_path)
            if original_clip.audio:
                video_clip = VideoFileClip(temp_video_path)
                final_clip = video_clip.set_audio(original_clip.audio)
                final_clip.write_videofile(output_path, codec='libx264',audio_codec='aac', logger=None)
            else:
                shutil.move(temp_video_path, output_path)
            self.logger.info(f"Successfully created final video at {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to process audio with moviepy: {e}, Saving video without audio.")
            shutil.move(temp_video_path, output_path)
        finally:
            if original_clip:
                original_clip.close()
            if video_clip:
                video_clip.close()
            if final_clip:
                final_clip.close()


        self.progress_callback(f"Done! Video saved to {os.path.basename(output_path)}")

    def process_video(self, video_path, prompt, api_manager, output_path):
        unique_frames, fps, temp_dir = self._extract_unique_frames(video_path)
        if unique_frames is None or not unique_frames:
            self.logger.error("No unique frames were extracted. Aborting Process.")
            self.progress_callback("Error: No frames found in video.")
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return

        processed_frames_info = self._process_frames_api(unique_frames, prompt, api_manager)
        self._reconstruct_video(video_path, processed_frames_info, fps, output_path, temp_dir)

        try:
            shutil.rmtree(temp_dir)
            self.logger.info(f"Successfully cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            self.logger.warning(f"Could not clean up temp directory {temp_dir}: {e}")
