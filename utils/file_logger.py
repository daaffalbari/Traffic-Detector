import datetime
import os

class TrafficLightLogger:
    """Manajemen logging untuk deteksi lampu lalu lintas"""
    def __init__(self, log_file='traffic_light_log.txt'):
        self.log_file = log_file
        self.reset_log_file()
    
    def reset_log_file(self):
        """Inisialisasi ulang file log"""
        with open(self.log_file, 'w') as f:
            f.write("Traffic Light Detection Log\n")
            f.write(f"Start Time: {datetime.datetime.now()}\n\n")
    
    def log_detection(self, color, frame_number, confidence=None):
        """Catat deteksi lampu lalu lintas"""
        timestamp = datetime.datetime.now()
        log_entry = (
            f"[Frame {frame_number}] {timestamp}: "
            f"{color.upper()} light detected"
        )
        
        if confidence is not None:
            log_entry += f" (Confidence: {confidence:.2f}%)"
        
        log_entry += "\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        return log_entry