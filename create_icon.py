import os
from PIL import Image, ImageDraw

def create_cctv_icon(output_path):
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    for size in sizes:
        w, h = size
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rounded background
        margin = int(w * 0.05)
        r = int(w * 0.22)
        
        # Dark obsidian background with cyan border
        draw.rounded_rectangle([margin, margin, w - margin, h - margin], radius=r, fill=(10, 15, 26, 255), outline=(0, 242, 254, 255), width=max(1, int(w * 0.04)))
        
        # Draw camera body (trapezoid / rectangle)
        cam_left = int(w * 0.25)
        cam_top = int(h * 0.35)
        cam_right = int(w * 0.62)
        cam_bottom = int(h * 0.65)
        draw.rounded_rectangle([cam_left, cam_top, cam_right, cam_bottom], radius=max(2, int(w * 0.04)), fill=(0, 242, 254, 255))
        
        # Camera lens cone
        lens_points = [
            (int(w * 0.62), int(h * 0.42)),
            (int(w * 0.78), int(h * 0.32)),
            (int(w * 0.78), int(h * 0.68)),
            (int(w * 0.62), int(h * 0.58))
        ]
        draw.polygon(lens_points, fill=(2, 132, 199, 255))
        
        # Infrared LED indicator dot (red/amber)
        led_x = int(w * 0.35)
        led_y = int(h * 0.45)
        led_r = max(2, int(w * 0.03))
        draw.ellipse([led_x - led_r, led_y - led_r, led_x + led_r, led_y + led_r], fill=(239, 68, 68, 255))
        
        # Mount stand
        stand_left = int(w * 0.38)
        stand_top = int(h * 0.65)
        stand_right = int(w * 0.48)
        stand_bottom = int(h * 0.80)
        draw.rectangle([stand_left, stand_top, stand_right, stand_bottom], fill=(148, 163, 184, 255))
        
        # Mount base
        base_left = int(w * 0.30)
        base_top = int(h * 0.78)
        base_right = int(w * 0.56)
        base_bottom = int(h * 0.84)
        draw.rounded_rectangle([base_left, base_top, base_right, base_bottom], radius=max(1, int(w * 0.02)), fill=(148, 163, 184, 255))
        
        images.append(img)
        
    images[0].save(output_path, format="ICO", sizes=sizes, append_images=images[1:])
    print(f"Icon saved: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    create_cctv_icon(out)
