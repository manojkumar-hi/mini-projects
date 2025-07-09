import qrcode

def generate_qr(data, filename="E:/edumoon/html_css_js/day18/qrcode.png"):
    # Create qr code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR code (1–40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )

    # Add data
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save it
    img.save(filename)
    print(f"✅ QR Code saved as: {filename}")

if __name__ == "__main__":
    user_input = input("Enter text or URL to generate QR code: ")
    generate_qr(user_input)
