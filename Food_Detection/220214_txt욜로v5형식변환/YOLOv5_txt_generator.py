# -*- coding: utf-8 -*- 
import os


def yolov5_txt_save(txt_name, single_or_multi, list_, case):
    '''
    input:
    txt_name -        생성할 txt파일 이름 
    single_or_multi - 레이블이 단일인지 멀티인지
    list_ -           txt에 작성할 좌표가 들어있는 리스트
    case -            1(norm_Center), 2(norm_TopLeft), 3(center), 4(topLeft)
    
    output:
    txt_path -        생성된 txt를 저장할 경로
    '''
    
    try:      
        if case == '1': # norm이 됐고 좌표가 Center 기준일 경우
            content,class_num, coord_ok = norm_Center(list_)
        
        elif case == '2': # norm이 됐고 좌표가 TopLeft 기준일 경우
            content,class_num, coord_ok = norm_TopLeft(list_)
        
        elif case == '3': # norm이 안 됐고 좌표가 center 기준일 경우
            content,class_num, coord_ok = center(list_)
        
        elif case == '4': # norm이 안 됐고 좌표가 topLeft 기준일 경우
            content,class_num, coord_ok = topLeft(list_)
        
        if coord_ok == 'Y': # 좌표들 중에 음수가 없는 정상이면 Y
            # txt파일을 저장할 path 설정
            path = '/Data/FoodDetection/data/food_detection/food_detection/yolov5_format'
            if single_or_multi == 'single':
                txt_path = os.path.join(path, single_or_multi, class_num, txt_name)
            elif single_or_multi == 'multi':
                txt_path = os.path.join(path, single_or_multi, txt_name)
        
            # txt 파일 작성
            with open(txt_path, 'w', encoding='UTF-8') as f:
                f.write(content)
            
            print('파일 생성 성공!')
            return txt_path, coord_ok
        
        elif coord_ok == 'N': # 좌표들 중에 음수가 있어서 비정상이면 N
            return coord_ok
        
    except:
        message = '파일 생성 실패'
        print(message)
        return message
        
        
'''case == '1', norm이 됐고 좌표가 Center 기준일 경우'''
def norm_Center(list_):
    
    content = '' # txt에 적을 내용
    coord_ok = 'Y' # 좌표들 중에 음수가 없는 정상이면 Y, 음수가 있어서 비정상이면 N
    for coord in list_:
        class_num = coord[0]
        x_center = float(coord[3])
        y_center = float(coord[4])
        w_bbox = float(coord[5])
        h_bbox = float(coord[6])
        
        if float(coord[3])<0 or float(coord[4])<0 or float(coord[5])<0 or float(coord[6])<0:
            coord_ok = 'N'
        
        content += str(class_num) + ' '
        content += str(round(x_center, 6)) + ' '
        content += str(round(y_center, 6)) + ' '
        content += str(round(w_bbox, 6)) + ' '
        content += str(round(h_bbox, 6)) + '\n'
        
    return content, class_num, coord_ok


'''case == '2', norm이 됐고 좌표가 TopLeft 기준일 경우'''
def norm_TopLeft(list_):
    
    content = '' # txt에 적을 내용
    coord_ok = 'Y' # 좌표들 중에 음수가 없는 정상이면 Y, 음수가 있어서 비정상이면 N
    for coord in list_:
        class_num = coord[0]
        x_center = float(coord[3])+float(coord[5])/2
        y_center = float(coord[4])+float(coord[6])/2
        w_bbox = float(coord[5])
        h_bbox = float(coord[6])
        
        if float(coord[3])<0 or float(coord[4])<0 or float(coord[5])<0 or float(coord[6])<0:
            coord_ok = 'N'
            
        content += str(class_num) + ' '
        content += str(round(x_center, 6)) + ' '
        content += str(round(y_center, 6)) + ' '
        content += str(round(w_bbox, 6)) + ' '
        content += str(round(h_bbox, 6)) + '\n'
        
    return content, class_num, coord_ok


'''case == '3', norm이 안 됐고 좌표가 center 기준일 경우'''
def center(list_):
        
    content = '' # txt에 적을 내용
    coord_ok = 'Y' # 좌표들 중에 음수가 없는 정상이면 Y, 음수가 있어서 비정상이면 N
    for coord in list_:
        class_num = coord[0]
        x_center = float(coord[3])/float(coord[1])
        y_center = float(coord[4])/float(coord[2])
        w_bbox = float(coord[5])/float(coord[1])
        h_bbox = float(coord[6])/float(coord[2])
        
        if float(coord[3])<0 or float(coord[4])<0 or float(coord[5])<0 or float(coord[6])<0:
            coord_ok = 'N'
            
        content += str(class_num) + ' '
        content += str(round(x_center, 6)) + ' '
        content += str(round(y_center, 6)) + ' '
        content += str(round(w_bbox, 6)) + ' '
        content += str(round(h_bbox, 6)) + '\n'
        
    return content, class_num, coord_ok


'''case == '4', norm이 안 됐고 좌표가 topLeft 기준일 경우'''
def topLeft(list_):
    
    content = '' # txt에 적을 내용
    coord_ok = 'Y' # 좌표들 중에 음수가 없는 정상이면 Y, 음수가 있어서 비정상이면 N
    for coord in list_:
        class_num = coord[0]
        x_center = (float(coord[3]) + float(coord[5])/2)/float(coord[1])
        y_center = (float(coord[4]) + float(coord[6])/2)/float(coord[2])
        w_bbox = float(coord[5])/float(coord[1])
        h_bbox = float(coord[6])/float(coord[2])
        
        if float(coord[3])<0 or float(coord[4])<0 or float(coord[5])<0 or float(coord[6])<0:
            coord_ok = 'N'
            
        content += str(class_num) + ' '
        content += str(round(x_center, 6)) + ' '
        content += str(round(y_center, 6)) + ' '
        content += str(round(w_bbox, 6)) + ' '
        content += str(round(h_bbox, 6)) + '\n'
        
    return content, class_num, coord_ok
