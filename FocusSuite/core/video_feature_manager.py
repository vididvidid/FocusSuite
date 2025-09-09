import os
import threading
from tkinter import filedialog, messagebox
from .video_processor import VideoProcessor

class VideoFeatureManager:
    """
    Orchestrate the video processing feature, acting as a bridge
    between the UI tab and the video processing core logic.
    """
    def __init__(self, logger, root, vision_api_manager):
        self.logger = logger
        self.root = root
        self.vision_api_manager = vision_api_manager

        self.video_path = None
        self.processing_thread = None
        self.ui_tab = None

    def register_ui_tabs(self, ui_tab):
        self.ui_tab = ui_tab

    def _update_log(self, message:str):
        if self.ui_tab:
            self.root.after(0,self.ui_tab.append_video_log, message)

    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="select a video file",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All files","*.*")]
        )
        if  file_path and self.ui_tab:
            self.video_path = file_path
            self.logger.info(f"Video file selected: {self.video_path}")
            self.ui_tab.video_path_label.config(text=os.path.basename(self.video_path))
        else:
            self.logger.info("Video selection cancelled.")

    def start_video_processing(self):
        if not self.ui_tab:
            self.logger.error("UI Tab not registered with VideoFeatureManager.")
            return

        if not self.video_path:
            messagebox.showwarning("Input Required", "Please select a video file first.")
            return

        prompt = self.ui_tab.video_prompt_entry.get().strip()
        if not prompt or "e.g.," in prompt:
            messagebox.showwarning("Input Required", "Please describe what you want to blur.")
            return

        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("In Progress", "A video is already being processed.")
            return


        path_without_ext, extension = os.path.splitext(self.video_path)
        output_path = f"{path_without_ext}_edited{extension}"
        
        self.logger.info(f"Output path automatically set to: {output_path}")
        self._update_log(f"Output will be saved as : {os.path.basename(output_path)}")


        self.ui_tab.start_video_button.config(state='disabled')
        self._update_log("Preparing to process video...")
        self.logger.info(f"Starting video processing for '{self.video_path}' with prompt '{prompt}'")

        self.processing_thread = threading.Thread(
            target=self._processing_worker,
            args=(self.video_path, prompt, output_path),
            daemon=True
        )
        self.processing_thread.start()

    def _processing_worker(self,video_path,prompt, output_path):
        try:
            processor = VideoProcessor(self.logger, self._update_log)
            processor.process_video(video_path, prompt, self.vision_api_manager,output_path)
            self.logger.info("Video processing finished successfully.")
            messagebox.showinfo('Sucess', f'Video processing complete!\n Saved to : {output_path}')
        except Exception as e:
            self.logger.error(f"An error occured in the video processing worker: {e}",exc_info=True)
            self._update_log(f"An unexpected error occurred: {e}")
            messagebox.showerror('Error', f'An unexpected error occurred during processing : {e}')
        finally:
            if self.ui_tab:
                self.root.after(0,self.ui_tab.start_video_button.config,{'state':'normal'})
