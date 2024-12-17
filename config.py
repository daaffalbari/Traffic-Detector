class Config:
    """Konfigurasi untuk sistem deteksi lampu lalu lintas"""
    COLOR_RANGES = {
        'red': {
            'ranges': [
                ((0, 100, 100), (10, 255, 255)),   # Rentang merah bawah
                ((160, 100, 100), (180, 255, 255)) # Rentang merah atas
            ],
            'color': (0, 0, 255) # Warna merah dalam format BGR
        },
        'yellow': {
            'ranges': [
                ((20, 100, 100), (35, 255, 255)) # Rentang kuning
            ],
            'color': (0, 255, 255) # Warna kuning dalam format BGR
        },
        'green': {
            'ranges': [
                ((40, 50, 50), (90, 255, 255)) # Rentang hijau
            ],
            'color': (0, 255, 0) # Warna hijau dalam format BGR
        }
    }

    # Prioritas warna: merah > kuning > hijau
    COLOR_PRIORITY = ['red', 'yellow', 'green']
    
    # Path default
    INPUT_VIDEO = './input/input.mp4'
    OUTPUT_VIDEO = './output/output.mp4'
    LOG_FILE = './logs/traffic_light_log.txt'
    
    # Parameter deteksi
    MIN_CONTOUR_AREA = 700
    MORPHOLOGY_KERNEL_SIZE = (5, 5)
    BRIGHTNESS_THRESHOLD = 50
    # Konfigurasi video
    FOURCC_CODEC = 'mp4v'
