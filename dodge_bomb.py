import os
import sys
import time
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

def gameover(screen: pg.Surface) -> None:
    game_set = pg.Surface((WIDTH, HEIGHT))  # 1 画面サイズの Surface を作る
    pg.draw.rect(game_set, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # 黒い矩形を描く
    game_set.set_alpha(255) #2 surfaceの透明度を設定する。（55の時は完全に不透明状態）
    game_set_fonto = pg.font.Font(None, 80) #3フォントのサイズを設定する。（第1引数 None は「システムのデフォルトフォント」を使うこと、第2引数 80 は文字サイズ（ピクセル）を表す）
    txt = game_set_fonto.render("Gameover",True, (255, 255, 255)) #白文字でGame Overと書かれた
    txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2)) #フォントを出力する場所をした。
    game_set.blit(txt,txt_rct) 
    game_set_bird = pg.image.load("fig/8.png") #4こうかとんの画像をロード
    bird_rct = game_set_bird.get_rect(center=(WIDTH//2 +200, HEIGHT//2)) #出力する場所
    bird_rct2 = game_set_bird.get_rect(center=(WIDTH//2 -200, HEIGHT//2)) #出力する場所
    game_set.blit(game_set_bird,bird_rct) #5 こうかとんの画像と場所をblit
    game_set.blit(game_set_bird,bird_rct2)
    screen.blit(game_set, [0,0])
    pg.display.update() #6 画面を更新
    time.sleep(5) #5秒まつ


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
#         bb_imgs.append(bb_img)
#         bb_accs = [a for a in range(1, 11)]
    
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
        for event in pg.event.get(): # イベント(ボタンを押すとか)処理
            if event.type == pg.QUIT: # QUITイベント(×ボタンが押されたら)が発生したら終了
                return
        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾が衝突したら
            gameover(screen)
            print("ゲームオーバー")
            return None# ゲーム終了
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
