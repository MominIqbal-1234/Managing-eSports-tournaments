from PIL import Image, ImageDraw, ImageFont

def write_text_on_image(text, output_path="output_image.jpg"):
    # Create a blank image
    image_width = 400
    image_height = 100
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Set font and size
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)

    # Write text on the image
    text = " ".join(map(str, text))
    draw.text((10, 10), text, font=font, fill="black")

    # Save the image
    image.save(output_path)

if __name__ == "__main__":
    data = [1, "Team1", 10, 45, 55]
    write_text_on_image(data)
