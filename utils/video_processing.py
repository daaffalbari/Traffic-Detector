import cv2
import os

class VideoProcessor:
    """Pemrosesan video untuk deteksi lampu lalu linats"""
    def __init__(self, config, color_detector, logger):
        self.config = config
        self.color_detector = color_detector
        self.logger = logger
    
    def process_video(self, input_path, output_path):
        """Proses video untuk deteksi lampu lalu linats"""
        # validated input video
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Video input tidak ditemukan: {input_path}")
        
        # Buka video
        cap = cv2.VideoCapture(input_path)
        
        # setting video writer
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # using codec yang lebih umum
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # deteksi lampu lalu lintas
                detected_lights = self.color_detector.detect_traffic_lights(frame)
                
                # created bounding box dan catat log
                for light in detected_lights:
                    x, y, w, h = light['bbox']
                    color = light['color']
                    color_rgb = light['color_rgb']
                    
                    # drawing bounding box
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color_rgb, 2)
                    cv2.putText(frame, color, (x, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_rgb, 2)
            
                    self.logger.log_detection(color, frame_count)
                
                out.write(frame)
                
                print(f"Memproses frame {frame_count}", end='\r')
        
        except Exception as e:
            print(f"\nKesalahan saat memproses video: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            cap.release()
            out.release()
        
        return frame_count