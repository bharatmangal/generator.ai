from PIL import Image, ImageDraw, ImageFont
import os

def convert_to_handwriting(text):

    os.makedirs("./static", exist_ok=True)

    # A4 dimensions in pixels at 300 DPI
    A4_WIDTH, A4_HEIGHT = 2480, 3508
    MARGIN = 150
    FONT_SIZE = 65
    LINE_SPACING = 80  # Adjust to match the register lines

    # Load the handwriting font
    font = ImageFont.truetype("./QEAntonyLark.ttf", FONT_SIZE)

    # Prepare for multi-page
    pages = []
    current_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    draw = ImageDraw.Draw(current_image)

    # Draw register lines
    # Horizontal blue lines
    for line_y in range(MARGIN + 100, A4_HEIGHT - MARGIN, LINE_SPACING):
        draw.line([(MARGIN, line_y), (A4_WIDTH - MARGIN, line_y)], fill="blue", width=2)

    # Vertical red margin line
    draw.line([(MARGIN + 100, MARGIN), (MARGIN + 100, A4_HEIGHT - MARGIN)], fill="red", width=4)

    # Horizontal red top margin line
    draw.line([(MARGIN, MARGIN + 100), (A4_WIDTH - MARGIN, MARGIN + 100)], fill="red", width=4)

    x, y = MARGIN + 120, MARGIN + 140  # Start text slightly below the horizontal red line

    # Split and write text
    for line in text.split("\n"):
        # Split lines that are too long to fit the page width
        while draw.textbbox((0, 0), line, font=font)[2] > A4_WIDTH - 2 * MARGIN - 120:
            # Break the line into two parts
            split_index = len(line) // 2
            line_part, line = line[:split_index], line[split_index:]
            draw.text((x, y), line_part, fill="black", font=font)
            y += LINE_SPACING

            # Create a new page if the current page is full
            if y + LINE_SPACING > A4_HEIGHT - MARGIN:
                pages.append(current_image)
                current_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
                draw = ImageDraw.Draw(current_image)

                # Redraw register lines for the new page
                for line_y in range(MARGIN + 100, A4_HEIGHT - MARGIN, LINE_SPACING):
                    draw.line([(MARGIN, line_y), (A4_WIDTH - MARGIN, line_y)], fill="blue", width=2)

                # Redraw vertical and horizontal red margin lines
                draw.line([(MARGIN + 100, MARGIN), (MARGIN + 100, A4_HEIGHT - MARGIN)], fill="red", width=4)
                draw.line([(MARGIN, MARGIN + 100), (A4_WIDTH - MARGIN, MARGIN + 100)], fill="red", width=4)

                y = MARGIN + 140

        # Draw remaining line
        draw.text((x, y), line, fill="black", font=font)
        y += LINE_SPACING

        # Create a new page if the current page is full
        if y + LINE_SPACING > A4_HEIGHT - MARGIN:
            pages.append(current_image)
            current_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
            draw = ImageDraw.Draw(current_image)

            # Redraw register lines for the new page
            for line_y in range(MARGIN + 100, A4_HEIGHT - MARGIN, LINE_SPACING):
                draw.line([(MARGIN, line_y), (A4_WIDTH - MARGIN, line_y)], fill="blue", width=2)

            # Redraw vertical and horizontal red margin lines
            draw.line([(MARGIN + 100, MARGIN), (MARGIN + 100, A4_HEIGHT - MARGIN)], fill="red", width=4)
            draw.line([(MARGIN, MARGIN + 100), (A4_WIDTH - MARGIN, MARGIN + 100)], fill="red", width=4)

            y = MARGIN + 140

    # Add the last page
    pages.append(current_image)

    # Save as PDF
    output = "./static/handwritten_assignment.pdf"
    pages[0].save(output, save_all=True, append_images=pages[1:])
    return output
