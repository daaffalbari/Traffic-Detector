import cv2
import numpy as np
import copy

class ColorDetector:
    """Deteksi warna lampu lalu lintas menggunakan metode HSV"""
    def __init__(self, config):
        self.config = config
    
    def enhance_low_light(self, frame):
        """Perbaiki pencahayaan untuk kondisi low-light"""
        frame_copy = np.copy(frame)
        
        try:
            # Konversi ke ruang warna LAB
            lab = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2LAB)
            
            # Pisahkan channel
            l, a, b = cv2.split(lab)
            
            # Implementasikan CLAHE hanya pada channel luminance (L)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l_enhanced = clahe.apply(l)
            
            # Gabungkan kembali channel
            lab_enhanced = cv2.merge([l_enhanced, a, b])
            
            # Konversi kembali ke BGR
            enhanced_frame = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
            
            return enhanced_frame
        
        except Exception as e:
            print(f"Kesalahan saat memperbaiki pencahayaan: {e}")
            return frame_copy
    
    def detect_traffic_lights(self, frame):
        """Deteksi warna lampu lalu lintas dalam frame"""
        try:
            enhanced_frame = self.enhance_low_light(frame)
            hsv_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2HSV)
            
            detected_lights = []
            
            # Deteksi untuk setiap warna
            for color_name, color_info in self.config.COLOR_RANGES.items():
                for color_range in color_info['ranges']:
                    # Buat mask untuk rentang warna
                    mask = cv2.inRange(hsv_frame, color_range[0], color_range[1])
                    
                    # Operasi morfologi untuk reduksi noise
                    kernel = np.ones(self.config.MORPHOLOGY_KERNEL_SIZE, np.uint8)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    
                    # Temukan kontur
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    for contour in contours:
                        if cv2.contourArea(contour) > self.config.MIN_CONTOUR_AREA:
                            x, y, w, h = cv2.boundingRect(contour)
                            roi = hsv_frame[y:y+h, x:x+w]  # Area of interest (ROI)
                            
                            # Tambahkan pengecekan kecerahan
                            brightness = np.mean(roi[:, :, 2])  # Channel V dari HSV
                            if brightness < self.config.BRIGHTNESS_THRESHOLD:
                                continue  # Abaikan area dengan brightness rendah
                            
                            # Hitung jumlah piksel dari semua warna
                            color_counts = {}
                            for c_name, c_info in self.config.COLOR_RANGES.items():
                                total_count = 0
                                for c_range in c_info['ranges']:
                                    mask_color = cv2.inRange(roi, c_range[0], c_range[1])
                                    total_count += np.sum(mask_color > 0)
                                color_counts[c_name] = total_count
                            
                            # Tentukan warna dominan
                            sorted_colors = sorted(
                                color_counts.items(), 
                                key=lambda item: (-item[1], self.config.COLOR_PRIORITY.index(item[0]))
                            )
                            
                            dominant_color = sorted_colors[0][0] if sorted_colors[0][1] > 0 else None
                            
                            if dominant_color:
                                detected_lights.append({
                                    'color': dominant_color,
                                    'bbox': [x, y, w, h],
                                    'color_rgb': self.config.COLOR_RANGES[dominant_color]['color']
                                })
            
            return detected_lights
        
        except Exception as e:
            print(f"Kesalahan saat mendeteksi lampu lalu lintas: {e}")
            return []
