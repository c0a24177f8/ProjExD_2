import os
import sys
import random   
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA ={
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),    
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct:pg.Rect)-> tuple[bool, bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    戻り値：判定結果（縦方向/横方向）
    画面内：True/画面外：False
    :param rct: 説明
    """
    tate, yoko = True, True # 初期値は画面内(True)
    if rct.left < 0 or rct.right > WIDTH:# 横方向のはみ出し判定
        yoko = False
    else:   
        yoko = True
    if rct.top < 0 or rct.bottom > HEIGHT:  # 縦方向のはみ出し判定  
        tate = False
    return tate, yoko

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空のSurface(縦20横20の画像)を生成
    bb_img.set_colorkey((0, 0, 0)) # 爆弾用のSurfaceの黒色部分を透明に設定
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 爆弾用のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect() # 爆弾用のRectを生成
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT) # 爆弾用のRectの中心座標をランダムに設定
    vx, vy = +5, +5  # 爆弾の横速度と縦速度を設定
    clock = pg.time.Clock() #  時間管理用Clockオブジェクトを生成
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦方向の移動量 
        kk_rct.move_ip(sum_mv) # こうかとんを移動させる
        if check_bound(kk_rct) != (True, True): # 画面外に出た場合
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面外に出たら移動を元に戻す
        screen.blit(kk_img, kk_rct) # こうかとんを画面に貼り付ける
        bb_rct.move_ip(vx, vy) # 爆弾を速度ベクトル(vx, vy)に基づいて移動させる
        screen.blit(bb_img, bb_rct) # 爆弾を画面に貼り付ける
        if check_bound(bb_rct) != (True, True): # 爆弾が画面外に出た場合
            if not check_bound(bb_rct)[0]:  # 縦方向にはみ出した場合
                vy *= -1
            if not check_bound(bb_rct)[1]:  # 横方向にはみ出した場合
                vx *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
