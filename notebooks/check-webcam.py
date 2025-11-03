"""
Script de diagnostic pour détecter les webcams disponibles
"""

import cv2
import os

def check_video_devices():
    """Vérifie les périphériques vidéo disponibles dans /dev"""
    print("=== Vérification des périphériques vidéo ===\n")
    
    video_devices = []
    if os.path.exists('/dev'):
        for device in os.listdir('/dev'):
            if device.startswith('video'):
                device_path = f'/dev/{device}'
                video_devices.append(device_path)
                print(f"✓ Trouvé: {device_path}")
    
    if not video_devices:
        print("✗ Aucun périphérique vidéo trouvé dans /dev/")
    
    return video_devices

def test_camera_indices(max_index=10):
    """Teste différents indices de caméra"""
    print("\n=== Test des indices de caméra OpenCV ===\n")
    
    available_cameras = []
    
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                print(f"✓ Caméra {i}: Disponible ({width}x{height})")
                available_cameras.append(i)
            else:
                print(f"○ Caméra {i}: Ouverte mais pas de frame")
            cap.release()
        else:
            # Ne pas afficher les échecs pour ne pas surcharger
            pass
    
    if not available_cameras:
        print("✗ Aucune caméra fonctionnelle détectée")
    
    return available_cameras

def test_backends():
    """Teste différents backends vidéo"""
    print("\n=== Test des backends disponibles ===\n")
    
    backends = [
        (cv2.CAP_V4L2, "V4L2 (Linux)"),
        (cv2.CAP_GSTREAMER, "GStreamer"),
        (cv2.CAP_FFMPEG, "FFmpeg"),
        (cv2.CAP_ANY, "Any (auto)"),
    ]
    
    working_backends = []
    
    for backend_id, backend_name in backends:
        try:
            cap = cv2.VideoCapture(0, backend_id)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"✓ {backend_name}: Fonctionne")
                    working_backends.append((backend_id, backend_name))
                else:
                    print(f"○ {backend_name}: Ouvert mais pas de frame")
                cap.release()
            else:
                print(f"✗ {backend_name}: Non disponible")
        except Exception as e:
            print(f"✗ {backend_name}: Erreur - {e}")
    
    return working_backends

def check_permissions():
    """Vérifie les permissions sur les périphériques vidéo"""
    print("\n=== Vérification des permissions ===\n")
    
    import subprocess
    
    try:
        # Vérifier les groupes de l'utilisateur
        result = subprocess.run(['groups'], capture_output=True, text=True)
        groups = result.stdout.strip()
        print(f"Groupes de l'utilisateur: {groups}")
        
        if 'video' in groups:
            print("✓ L'utilisateur est dans le groupe 'video'")
        else:
            print("✗ L'utilisateur n'est PAS dans le groupe 'video'")
            print("  Solution: sudo usermod -aG video $USER (puis redémarrer)")
    except Exception as e:
        print(f"Impossible de vérifier les groupes: {e}")

def main():
    print("=" * 60)
    print("DIAGNOSTIC WEBCAM")
    print("=" * 60)
    
    # 1. Vérifier les périphériques
    video_devices = check_video_devices()
    
    # 2. Tester les indices de caméra
    available_cameras = test_camera_indices()
    
    # 3. Tester les backends
    working_backends = test_backends()
    
    # 4. Vérifier les permissions
    check_permissions()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    if available_cameras:
        print(f"\n✓ {len(available_cameras)} caméra(s) détectée(s): {available_cameras}")
        print(f"\nUtilisez: WebcamInterface(camera_index={available_cameras[0]})")
    else:
        print("\n✗ Aucune caméra fonctionnelle détectée")
        print("\nActions possibles:")
        print("1. Vérifiez qu'une webcam est branchée")
        print("2. Vérifiez les permissions: sudo usermod -aG video $USER")
        print("3. Installez les dépendances: sudo apt-get install v4l-utils")
        print("4. Listez les devices: v4l2-ctl --list-devices")

if __name__ == "__main__":
    main()