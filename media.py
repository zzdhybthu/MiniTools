import Bilibili_video_download.bilibili_video_download_v2 as v_bili # Bilibili
import musicdownloader.musicdownloader as a_qq_nec # QQ & NetEase Cloud
import mp4tomp3.mp4tomp3 as t_mp4_mp3


def is_value_in_range(value,min,max):
    try:
        number=int(value)
        if number>=min and number<max:
            return number
    except ValueError:
        pass
    return 0

def input_value():
    return input('''
\033[34m 1. \033[32m Bilibili video
\033[34m 2. \033[32m QQ & NetEase Cloud music
\033[34m 3. \033[32m mp4tomp3
''')

value=input_value()
while value!='q':
    number=is_value_in_range(value,1,4)
    try:
        if number==0:
            print("Error!\n")
        elif number==1:
            v_bili.default_main()
        elif number==2:
            a_qq_nec.default_main()
        elif number==3:
            t_mp4_mp3.default_main()
    except:
        print("Fail!\n")

    value=input_value()
