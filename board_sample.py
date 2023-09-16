from PIL import Image, ImageDraw
import os
image = Image.new("RGB", (600, 600), "WHITE")
draw = ImageDraw.Draw(image)

board = [
    [1, -1, -1, -1, -1],
    [-1,  0,  0,  0, -1],
    [ 1,  0,  0,  0, -1],
    [ 1,  0,  0,  0,  1],
    [ 1,  1,  1,  1,  1]
]


draw.line((100, 100, 500, 100), fill="black", width=3)
draw.line((100, 200, 500, 200), fill="black", width=3)
draw.line((100, 300, 500, 300), fill="black", width=3)
draw.line((100, 400, 500, 400), fill="black", width=3)
draw.line((100, 500, 500, 500), fill="black", width=3)
draw.line((100, 100, 100, 500), fill="black", width=3)

draw.line((200, 100, 200, 500), fill="black", width=3)
draw.line((300, 100, 300, 500), fill="black", width=3)
draw.line((400, 100, 400, 500), fill="black", width=3)
draw.line((500, 100, 500, 500), fill="black", width=3)
draw.line((100, 100, 500, 500), fill="black", width=3)
draw.line((100, 500, 500, 100), fill="black", width=3)

draw.line((100, 300, 300, 100), fill="black", width=3)
draw.line((300, 100, 500, 300), fill="black", width=3)
draw.line((500, 300, 300, 500), fill="black", width=3)
draw.line((300, 500, 100, 300), fill="black", width=3)

x = 80
y = 80 
for row in range(len(board)):
    for column in range(len(board[0])):
        if board[row][column] == -1:
            draw.ellipse((x, y, x + 40, y + 40), fill="red", outline="red")
        elif board[row][column] == 1:
            draw.ellipse((x, y, x + 40, y + 40), fill="blue", outline="blue")
        else:
            pass
        x = x + 100
    x = 80
    y = y + 100

cwd = os.getcwd()
print(cwd)
img_dir = cwd + "/static/upload_video"
print(img_dir)


image.save(f"{img_dir}/chessboard.png", "PNG")