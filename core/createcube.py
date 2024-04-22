from PIL import Image
from pathlib import PurePath

def cube(adjacences, sizex, sizey):
    corners = [(0,1,2), (2,3,4), (4,5,6), (6,7,0)]
    cubetype = []

    for corner in corners:
        if adjacences[corner[0]] == 1 and adjacences[corner[2]] == 1:
            if adjacences[corner[1]] == 0:
                # Vide : 0, Point : 1, Ligne sur le 0 : 2, Ligne sur le 2 : 3, Coin : 4
                cubetype.append(1)
            else:
                cubetype.append(0)
        elif adjacences[corner[0]] == 0 and adjacences[corner[2]] == 0:
            cubetype.append(4)
        elif adjacences[corner[0]] == 1:
            cubetype.append(2)
        else:
            cubetype.append(3)
    
    imagecubefinal = Image.new("RGBA", (sizex, sizey), (0, 0, 0, 0))
    cubeimage = []

    for corner in range(len(cubetype)):
        match cubetype[corner]:
            case 0:
                cubeimage.append(Image.open(PurePath("images/level/cube_milieu.png")))
            case 1:
                cubeimage.append(Image.open(PurePath("images/level/cube_point.png")))
                match corner:
                    case 1:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    case 2:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    case 3:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            case 2:
                cubeimage.append(Image.open(PurePath("images/level/cube_bord.png")))
                match corner:
                    case 1:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    case 2:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    case 3:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            
            case 3:
                cubeimage.append(Image.open(PurePath("images/level/cube_bord.png")))
                match corner:
                    case 1:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    case 2:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    case 3:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                cubeimage[-1] = cubeimage[-1].rotate(90)

            case 4:
                cubeimage.append(Image.open(PurePath("images/level/cube_coint.png")))
                match corner:
                    case 1:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    case 2:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    case 3:
                        cubeimage[-1] = cubeimage[-1].transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    
    imagecubefinal.paste(cubeimage[0], (0, 0))
    imagecubefinal.paste(cubeimage[1], (25, 0))
    imagecubefinal.paste(cubeimage[2], (25, 25))
    imagecubefinal.paste(cubeimage[3], (0, 25))

    return imagecubefinal.tobytes()
