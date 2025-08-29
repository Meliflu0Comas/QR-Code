from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask
from PIL import Image, ImageDraw
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_qr():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data received'}), 400
            
        url = data.get('url', '').strip()
        if not url:
            return jsonify({'success': False, 'error': 'URL cannot be empty'}), 400
            
        style = data.get('style', 'square')
        color = data.get('color', '#000000')
        background = data.get('background', '#FFFFFF')
        size = int(data.get('size', 10))
        border = int(data.get('border', 4))
        error_correction = data.get('error_correction', 'M')
        gradient_type = data.get('gradient_type', 'none')
        gradient_color = data.get('gradient_color', '#FF0000')
        
        print(f"Processing QR for URL: '{url}', Style: {style}")
        
        # Convert hex colors to RGB tuples
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        color_rgb = hex_to_rgb(color)
        background_rgb = hex_to_rgb(background)
        gradient_color_rgb = hex_to_rgb(gradient_color)
        
        print(f"Colors converted - Foreground: {color_rgb}, Background: {background_rgb}, Gradient: {gradient_color_rgb}")
        
        # Set error correction level
        error_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        print(f"Creating QR code object...")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
            box_size=size,
            border=border,
        )
        
        qr.add_data(url)
        print(f"Added data to QR code")
        
        qr.make(fit=True)
        print(f"QR code make() completed")
        
        # Choose module drawer style
        print(f"Selecting module drawer for style: {style}")
        module_drawers = {
            'square': SquareModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'gapped': GappedSquareModuleDrawer()
        }
        
        module_drawer = module_drawers.get(style, SquareModuleDrawer())
        print(f"Module drawer selected: {type(module_drawer).__name__}")
        
        # Choose color mask
        print(f"Setting up color mask, gradient_type: {gradient_type}")
        if gradient_type == 'radial':
            color_mask = RadialGradiantColorMask(back_color=background_rgb, center_color=color_rgb, edge_color=gradient_color_rgb)
        elif gradient_type == 'square':
            color_mask = SquareGradiantColorMask(back_color=background_rgb, center_color=color_rgb, edge_color=gradient_color_rgb)
        else:
            color_mask = SolidFillColorMask(front_color=color_rgb, back_color=background_rgb)
        
        print(f"Color mask created: {type(color_mask).__name__}")
        
        # Generate QR code image
        print(f"Generating QR code image...")
        qr_image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )
        print(f"QR image generated successfully")
        
        # Convert to base64 for web display
        print(f"Converting to base64...")
        img_buffer = io.BytesIO()
        qr_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        print(f"Base64 conversion completed")
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(f"ERROR TYPE: {type(e).__name__}")
        import traceback
        print(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'{type(e).__name__}: {str(e)}'
        }), 400

@app.route('/generate-svg', methods=['POST', 'OPTIONS'])
def generate_svg():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data received'}), 400
            
        url = data.get('url', '').strip()
        if not url:
            return jsonify({'success': False, 'error': 'URL cannot be empty'}), 400
            
        # Get all the same parameters as PNG generation
        style = data.get('style', 'square')
        color = data.get('color', '#000000')
        background = data.get('background', '#ffffff')
        size = int(data.get('size', 10))
        border = int(data.get('border', 4))
        error_correction = data.get('error_correction', 'M')
        gradient_type = data.get('gradient_type', 'none')
        gradient_color = data.get('gradient_color', '#ff0000')
        
        print(f"Generating SVG for URL: '{url}', Style: {style}")
        
        # Convert hex colors to RGB tuples (same as PNG)
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        color_rgb = hex_to_rgb(color)
        background_rgb = hex_to_rgb(background)
        gradient_color_rgb = hex_to_rgb(gradient_color)
        
        # Set error correction level
        error_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        
        # Generate the styled PNG version first, then convert to SVG
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
            box_size=size,
            border=border,
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        # Use the same styling system as PNG
        from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer
        from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask
        
        module_drawers = {
            'square': SquareModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'gapped': GappedSquareModuleDrawer()
        }
        
        module_drawer = module_drawers.get(style, SquareModuleDrawer())
        
        # Choose color mask (same as PNG)
        if gradient_type == 'radial':
            color_mask = RadialGradiantColorMask(back_color=background_rgb, center_color=color_rgb, edge_color=gradient_color_rgb)
        elif gradient_type == 'square':
            color_mask = SquareGradiantColorMask(back_color=background_rgb, center_color=color_rgb, edge_color=gradient_color_rgb)
        else:
            color_mask = SolidFillColorMask(front_color=color_rgb, back_color=background_rgb)
        
        # Generate styled image first (PNG)
        styled_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )
        
        # Convert the styled PIL image to SVG
        # Get the image size
        img_width, img_height = styled_img.size
        
        # Create SVG header
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{img_width}" height="{img_height}" viewBox="0 0 {img_width} {img_height}">'''
        
        # Add background
        svg_content += f'<rect width="{img_width}" height="{img_height}" fill="rgb{background_rgb}"/>'
        
        # Convert PIL image to pixel data and create SVG paths
        pixels = styled_img.load()
        
        # Group consecutive pixels of the same color to create more efficient paths
        for y in range(img_height):
            current_color = None
            path_start = None
            
            for x in range(img_width):
                pixel = pixels[x, y]
                if isinstance(pixel, tuple) and len(pixel) >= 3:
                    pixel_color = pixel[:3]
                else:
                    pixel_color = background_rgb
                
                if pixel_color != background_rgb:  # Only draw non-background pixels
                    if current_color != pixel_color:
                        if current_color is not None and path_start is not None:
                            # End previous path
                            svg_content += f'<rect x="{path_start}" y="{y}" width="{x - path_start}" height="1" fill="rgb{current_color}"/>'
                        current_color = pixel_color
                        path_start = x
                else:
                    if current_color is not None and path_start is not None:
                        # End current path
                        svg_content += f'<rect x="{path_start}" y="{y}" width="{x - path_start}" height="1" fill="rgb{current_color}"/>'
                    current_color = None
                    path_start = None
            
            # End line if needed
            if current_color is not None and path_start is not None:
                svg_content += f'<rect x="{path_start}" y="{y}" width="{img_width - path_start}" height="1" fill="rgb{current_color}"/>'
        
        svg_content += '</svg>'
        
        # Encode as base64 for data URL
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode()
        
        return jsonify({
            'success': True,
            'svg': f'data:image/svg+xml;base64,{svg_base64}',
            'svg_content': svg_content
        })
        
    except Exception as e:
        print(f"SVG ERROR: {str(e)}")
        import traceback
        print(f"SVG TRACEBACK: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'{type(e).__name__}: {str(e)}'
        }), 400

@app.route('/download')
def download_qr():
    # This endpoint could be enhanced to store and serve generated QR codes
    pass

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # For production (WSGI servers)
    application = app