import os
import sys
import traceback

from config import Config
from utils.color_detection import ColorDetector
from utils.video_processing import VideoProcessor
from utils.file_logger import TrafficLightLogger


def main():
    """Titik masuk utama untuk sistem deteksi lampu lalu lintas"""
    try:
        input_video = sys.argv[1] if len(sys.argv) > 1 else Config.INPUT_VIDEO
        
        if not os.path.exists(input_video):
            print(f"Error: File video {input_video} tidak ditemukan!")
            print("Gunakan: python main.py [path_video]")
            sys.exit(1)
        
        # update konfigurasi dengan video input dinamis
        Config.INPUT_VIDEO = input_video
        
        # Inisialisasi komponen
        logger = TrafficLightLogger(Config.LOG_FILE)
        color_detector = ColorDetector(Config)
        video_processor = VideoProcessor(Config, color_detector, logger)
        
        processed_frames = video_processor.process_video(
            Config.INPUT_VIDEO, 
            Config.OUTPUT_VIDEO
        )
        
        print("\nVideo berhasil diproses:")
        print(f"- Total frame: {processed_frames}")
        print(f"- Input video: {Config.INPUT_VIDEO}")
        print(f"- Output video: {Config.OUTPUT_VIDEO}")
        print(f"- Log file: {Config.LOG_FILE}")
    
    except Exception as e:
        print("\nTerjadi kesalahan:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()