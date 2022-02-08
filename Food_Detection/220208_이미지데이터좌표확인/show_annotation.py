#### txt 파일 내용이 ######################################################
#### 480 360 36 51 379 175 363 ############################################
#### 3024, 4032, 685, 1234, 1796, 1895, None ##############################
#### 600, 400, 2, 1, 588, 398, 가리비구이 #################################
#### 300,300,2,4,291,293,간장게장 #########################################
#### 이런 식이라서 정규표현식으로 띄어쓰기와 ,가 아닌 걸 잡는다. ##########
p = re.compile('[^ ,]+')

def imgTxtCheck(img, txt):
    
    print(f'\nimg 경로: {img},\ntxt 경로: {txt}\n')
    
    # class_dic.txt를 딕셔너리로 가져오기
    class_dic = {}
    f = open('./class_dic.txt','r')
    while True:
        line = f.readline()
        if not line : break
#         print(line.split(':')[0], line.split(':')[1][:-1])
        class_dic[int(line.split(':')[0])] = line.split(':')[1][:-1]
    f.close()
    
    if os.path.isfile(img) and os.path.isfile(txt):
        print('img,txt 파일 존재 확인')
        
        img = Image.open(img)
        
#######################################################
######## 이미지가 자동으로 회전되는 문제 해결 #########
######## https://www.jongho.dev/development/%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C-%EC%8B%9C-%ED%9A%8C%EC%A0%84%EC%97%90-%EA%B4%80%ED%95%B4%EC%84%9C/
        img = ImageOps.exif_transpose(img)
    
        w, h = float(img.size[0]), float(img.size[1])
#         print('img.size: ', w, h)
        
        with open(txt, "r", encoding='utf-8') as text:
            lines = text.readlines()
            if len(lines) > 1:
                print('멀티 레이블이다!')
                
            # 멀티 레이블일 때 멀티 바운딩 박스를 한 이미지에 표시하기 위한 리스트 
            box = []
            for num in range(len(lines)):
                line = lines[num].replace('\n', '')
                m_line = p.findall(line)
                print('txt 내용: ', m_line)
                
                # 노말라이제이션 된 것은 길이가 5이다.
                if len(m_line) == 5:
                    normalization = True
                    print('Normalization 완료')
                    
                    label, x_coord, y_coord, bbox_w, bbox_h  = \
                    class_dic[int(m_line[0])], float(m_line[1]), float(m_line[2]), float(m_line[3]), float(m_line[4])
                    
#                     print('label, x_coord, y_coord, bbox_w, bbox_h: ', label, x_coord, y_coord, bbox_w, bbox_h)
                    print('label: ', label)

                    #좌상단 기준의 x,y일 경우
                    topLeft = [(x_coord+bbox_w/2)*w, (y_coord+bbox_h/2)*h, bbox_w*w, bbox_h*h, label]
                                        
                    # 센터 기준의 x,y일 경우
                    center = [x_coord*w, y_coord*h, bbox_w*w, bbox_h*h, label]
                    
                # 노말라이제이션 안된 것들은 길이가 5 이상이다.
                else:
                    normalization = False
                    print('Normalization 안됨')
                    
##############################################################################
####### 레이블에 ' ' 띄어쓰기가 있을 경우 문제 해결 ##########################
####### '_'.join(m_line[6:])으로 6 이후의 레이블들을 _로 연결해준다.  ########
                    label, w_txt, h_txt, x_coord, y_coord, bbox_w, bbox_h  = \
                    '_'.join(m_line[6:]), float(m_line[0]), float(m_line[1]), float(m_line[2]), \
                    float(m_line[3]), float(m_line[4]), float(m_line[5])
                    
                    if w_txt != w or h_txt != h:
                        print('이미지 사이즈 잘못 측정됨')
                    
                    if label == 'None':
                        label = txt.split('/')[-1]
                        print('label: ', label)
                        
                    else:
                        print('label: ', label)
                    
#                     #좌상단 기준의 x,y일 경우
                    topLeft = [x_coord+bbox_w/2, y_coord+bbox_h/2, bbox_w, bbox_h, label]
                    
                    # 센터 기준의 x,y일 경우
                    center = [x_coord, y_coord, bbox_w, bbox_h, label]
            
#                 print('Top Left 기준일 경우: ', topLeft, '\n' \
#                       'Center 기준일 경우: ', center)
                
                ###### append로 여러개 한꺼번에 추가할 때는 extend를 사용하자!!###
                ######  https://www.codeit.kr/community/threads/12373 ############
                box.extend([topLeft, center])
        
#             print(box)
            n_cols = 2
            fig, axs = plt.subplots(figsize=(8*n_cols, 8), nrows=1, ncols=n_cols)

#             print('\nbox 내용: ', box)
            for ind, coord in enumerate(box):
#                 print(ind, coord)
                # Top Left를 왼쪽에 표시하고 Center는 오른쪽에 표시한다.
                if ind % 2==0:
                    ind = 0
                    axs[ind].set_title('Coordinate : Top Left')
                else:
                    ind = 1
                    axs[ind].set_title('Coordinate : Center')
        
                Korim = np.array(img, dtype=np.uint8)
                axs[ind].imshow(Korim)
            
                newPt = [[coord[0]-coord[2]/2, coord[1]+coord[3]/2], [coord[0]+coord[2]/2, coord[1]+coord[3]/2], \
                         [coord[0]+coord[2]/2, coord[1]-coord[3]/2], [coord[0]-coord[2]/2, coord[1]-coord[3]/2]]
                
                # axs.text(1.05, 10.05, coord[4], fontsize=30, horizontalalignment='left', verticalalignment='bottom', bbox=props, fontproperties=font_name)
                # https://runebook.dev/ko/docs/matplotlib/_as_gen/matplotlib.axes.axes.text
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                # x = coord[0]-center_X, y = coord[1]-center_Y, s = coord[4]-label
                axs[ind].text(coord[0], coord[1], coord[4], fontsize=15, horizontalalignment='center', verticalalignment='center', bbox=props, fontproperties=font_name)    
                rect = Polygon(newPt, linewidth=1.5, edgecolor='r', facecolor='none')
                axs[ind].add_patch(rect)
                
            # 좌표확인_{label}.png 이름 저장
            output_name = f'./좌표확인_{label}.png'
            plt.savefig(output_name)
                
            # 현재 파일/디렉토리 위치 확인 및 변경
            # https://velog.io/@stu_dy/Python-%ED%98%84%EC%9E%AC-%ED%8C%8C%EC%9D%BC%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC-%EC%9C%84%EC%B9%98-%ED%99%95%EC%9D%B8-%EB%B0%8F-%EB%B3%80%EA%B2%BD
            output_path = os.path.realpath(f'./좌표확인_{label}.png')
#             print('\n좌표확인 이미지 저장 위치: ', output_path)
            
            return output_name, output_path, box, normalization
    else:
        return print(f'경로가 잘못 되었다!!\nimg 존재: {os.path.isfile(img)}, txt 존재: {os.path.isfile(txt)}')