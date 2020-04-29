from Engine.Filter import Instance
from Engine.Penguin import Penguin
from Engine.Matchmaking import addToQueue
import json

queue = []

@Instance.register("/intro_anim_done")
def versionhandler(client, arg):
    print(client)
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"type":"immediateAction","action":"setWorldId","worldId":1510202}')
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"type":"immediateAction","action":"setBaseAssetUrl","baseAssetUrl":"http://media.localhost/game/mpassets/"}')
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"type":"immediateAction","action":"setFontPath","defaultFontPath":"http://media.localhost/game/mpassets//fonts/"}')
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"type":"playAction","action":"skinRoomToRoom","url":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/../assets/cjsnow_loadingscreenassets.swf", "className":"", "variant":0 }')
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","assetPath":"","initializationPayload":[null],"layerName":"bottomLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowerrorhandler.swf","xPercent":0,"yPercent":0}')
    client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","assetPath":"","initializationPayload":{"game":"snow","name":"'+str(client.name)+'","powerCardsFire":'+str(client.getPowerCards("fire"))+',"powerCardsSnow":'+str(client.getPowerCards("snow"))+',"powerCardsWater":'+str(client.getPowerCards("water"))+'},"layerName":"topLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowplayerselect.swf","xPercent":0,"yPercent":0}')

@Instance.register("Framework")
def readyhandler(client, arg):
    try:
        parsedJson = json.loads(arg)
    except:
        print("Error parsing json")
        return
    if parsedJson['triggerName']=="mmElementSelected":
        client.element = parsedJson['element']
        client.tipsEnabled = parsedJson['tipMode']
        addToQueue(client)
    if 'action' in parsedJson:
        if parsedJson['action'] == "funnel_prepare_to_battle_4":
            client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"type":"playAction","action":"closeWindow","targetWindow":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowplayerselect.swf"}')
            client.sendLine("[O_GONE]|4")
            client.sendLine("[W_PLACE]|1:10001|8|1")
            client.sendLine("[W_INPUT]|use|0:10|2|3|0|use|")
            client.sendLine("[W_INPUT]|touch-the-terrain|0:8600033|1|6|0|path_terrain|")
            client.sendLine("[W_INPUT]|mouse-the-terrain|0:8600033|1|3|0|path_terrain|")
            client.sendLine("[P_MAPBLOCK]|t|1|1|iVBORw0KGgoAAAANSUhEUgAAAAkAAAAFCAAAAACyOJm3AAAAHUlEQVQImWNgZeRkZARidgZGCGBnZ2CFMVHEoOoADJEAhIsKxDUAAAAASUVORK5CYII=")
            client.sendLine("[P_MAPBLOCK]|h|1|1|iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAAAAADfm1AaAAAADklEQVQImWNogAMG8pgA3m8eAacnkzQAAAAASUVORK5CYII=")
            client.sendLine("[P_ZOOMLIMIT]|-1.000000|-1.000000")
            client.sendLine("[P_RENDERFLAGS]|0|48")
            client.sendLine("[P_SIZE]|9|5")
            client.sendLine("[P_VIEW]|5")
            client.sendLine("[P_START]|4.5|2.5|0")
            client.sendLine("[P_LOCKVIEW]|0")
            client.sendLine("[P_TILESIZE]|100")
            client.sendLine("[P_ELEVSCALE]|0.031250")
            client.sendLine("[P_RELIEF]|1")
            client.sendLine("[P_LOCKSCROLL]|1|0|0|573321786")
            client.sendLine("[P_HEIGHTMAPSCALE]|0.078125|128")
            client.sendLine("[P_HEIGHTMAPDIVISIONS]|1")
            client.sendLine("[P_CAMERA3D]|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|0|0.000000|0.000000|0.000000|0.000000|0.000000|0.000000|864397819904.000000|0.000000|0|0")
            client.sendLine("[UI_BGCOLOR]|0|0|0")
            client.sendLine("[P_DRAG]|0")
            client.sendLine("[P_CAMLIMITS]|0|0|0|0")
            client.sendLine("[P_LOCKRENDERSIZE]|0|1024|768")
            client.sendLine("[P_LOCKOBJECTS]|0")
            client.sendLine("[UI_BGSPRITE]|0:-1|0|1.000000|1.000000")
            client.sendLine("[P_TILE]|0||0|0|1|0:2|Empty Tile|0|0|0|0:7940012")
            client.sendLine("[P_TILE]|1||0|0|1|0:2|open|0|0|0|0:7940013")
            client.sendLine("[P_TILE]|2||0|0|1|0:3|enemy|0|0|0|0:7940014")
            client.sendLine("[P_TILE]|3||0|0|1|0:4|penguin|0|0|0|0:7940015")
            client.sendLine("[P_TILE]|4||0|0|1|0:100002|penguin_spawn_occupied|0|0|0|0:7940016")
            client.sendLine("[P_TILE]|5||0|0|1|0:6|penguin_spawn_unoccupied|0|0|0|0:7940017")
            client.sendLine("[P_TILE]|7||0|0|1|0:10003|enemy_spawn_unoccupied|0|0|0|0:7940018")
            client.sendLine("[P_TILE]|8||0|0|1|0:10004|enemy_spawn_occupied|0|0|0|0:7940019")
            client.sendLine("[P_TILE]|9||0|0|1|0:10005|obstacle|0|0|0|0:7940020")
            client.sendLine("[P_PHYSICS]|0|0|0|0|0|0|0|1")
            client.sendLine("[P_ASSETSCOMPLETE]|0|0")
            client.sendLine("[O_HERE]|4|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_HERE]|9|0:1|10.7667|5.92222|0|1|0|0|0|Actor5|0:30021|0|0|0")
            client.sendLine("[O_HERE]|10|0:1|4.48869|-1.11106|0|1|0|0|0|Actor6|0:10002|0|0|0")
            client.sendLine("[O_HERE]|11|0:1|4.5|6.1|0|1|0|0|0|Actor7|0:6740006|0|0|0")
            client.sendLine("[P_CAMERA]|4.5|2.49333|0|0|1")
            client.sendLine("[P_ZOOM]|1.000000")
            client.sendLine("[P_LOCKZOOM]|1")
            client.sendLine("[P_LOCKCAMERA]|1")
            client.sendLine("[O_PLAYER]|4|")
        if parsedJson['triggerName']=="roomToRoomComplete":
            client.sendLine("[S_LOADSPRITE]|0:100307")
            client.sendLine("[S_LOADSPRITE]|0:100319")
            client.sendLine("[S_LOADSPRITE]|0:100303")
            client.sendLine("[S_LOADSPRITE]|0:100308")
            client.sendLine("[S_LOADSPRITE]|0:100318")
            client.sendLine("[S_LOADSPRITE]|0:100306")
            client.sendLine("[S_LOADSPRITE]|0:100310")
            client.sendLine("[S_LOADSPRITE]|0:100312")
            client.sendLine("[S_LOADSPRITE]|0:100315")
            client.sendLine("[S_LOADSPRITE]|0:100316")
            client.sendLine("[S_LOADSPRITE]|0:100317")
            client.sendLine("[S_LOADSPRITE]|0:100313")
            client.sendLine("[S_LOADSPRITE]|0:100314")
            client.sendLine("[S_LOADSPRITE]|0:100302")
            client.sendLine("[S_LOADSPRITE]|0:100299")
            client.sendLine("[S_LOADSPRITE]|0:100240")
            client.sendLine("[S_LOADSPRITE]|0:100241")
            client.sendLine("[S_LOADSPRITE]|0:100309")
            client.sendLine("[S_LOADSPRITE]|0:100320")
            client.sendLine("[S_LOADSPRITE]|0:100304")
            client.sendLine("[S_LOADSPRITE]|0:1840011")
            client.sendLine("[S_LOADSPRITE]|0:1840012")
            client.sendLine("[S_LOADSPRITE]|0:1840010")
            client.sendLine("[S_LOADSPRITE]|0:100307")
            client.sendLine("[S_LOADSPRITE]|0:100319")
            client.sendLine("[S_LOADSPRITE]|0:100303")
            client.sendLine("[S_LOADSPRITE]|0:100308")
            client.sendLine("[S_LOADSPRITE]|0:100318")
            client.sendLine("[S_LOADSPRITE]|0:100306")
            client.sendLine("[S_LOADSPRITE]|0:100310")
            client.sendLine("[S_LOADSPRITE]|0:100312")
            client.sendLine("[S_LOADSPRITE]|0:100315")
            client.sendLine("[S_LOADSPRITE]|0:100316")
            client.sendLine("[S_LOADSPRITE]|0:100317")
            client.sendLine("[S_LOADSPRITE]|0:100313")
            client.sendLine("[S_LOADSPRITE]|0:100314")
            client.sendLine("[S_LOADSPRITE]|0:100302")
            client.sendLine("[S_LOADSPRITE]|0:100299")
            client.sendLine("[S_LOADSPRITE]|0:100240")
            client.sendLine("[S_LOADSPRITE]|0:100241")
            client.sendLine("[S_LOADSPRITE]|0:100309")
            client.sendLine("[S_LOADSPRITE]|0:100320")
            client.sendLine("[S_LOADSPRITE]|0:100304")
            client.sendLine("[S_LOADSPRITE]|0:1840011")
            client.sendLine("[S_LOADSPRITE]|0:1840012")
            client.sendLine("[S_LOADSPRITE]|0:1840010")
            client.sendLine("[O_HERE]|12|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
        if parsedJson['triggerName']=="roomToRoomMinTime":
            client.sendLine('[UI_CLIENTEVENT]|101|receivedJson|{"action":"loadWindow","assetPath":"","initializationPayload":[null],"layerName":"bottomLayer","loadDescription":"","type":"playAction","windowUrl":"http://media.localhost/game/mpassets/minigames/cjsnow/en_US/deploy/swf/ui/windows/cardjitsu_snowclose.swf","xPercent":1,"yPercent":0}')
            client.sendLine("[O_HERE]|13|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_SPRITE]|10|0:100380|0|")
            client.sendLine("[O_SPRITE]|11|0:1|0|")
            client.sendLine("[O_HERE]|14|0:1|0.5|0.9998|0|1|0|0|0|Actor14|0:30020|0|1|0")
            client.sendLine("[O_HERE]|15|0:1|0.5|1.9998|0|1|0|0|0|Actor15|0:30020|0|1|0")
            client.sendLine("[O_HERE]|16|0:1|0.5|2.9998|0|1|0|0|0|Actor16|0:30020|0|1|0")
            client.sendLine("[O_HERE]|17|0:1|0.5|3.9998|0|1|0|0|0|Actor17|0:30020|0|1|0")
            client.sendLine("[O_HERE]|18|0:1|0.5|4.9998|0|1|0|0|0|Actor18|0:30020|0|1|0")
            client.sendLine("[O_HERE]|19|0:1|1.5|0.9998|0|1|0|0|0|Actor19|0:30020|0|1|0")
            client.sendLine("[O_HERE]|20|0:1|1.5|1.9998|0|1|0|0|0|Actor20|0:30020|0|1|0")
            client.sendLine("[O_HERE]|21|0:1|1.5|2.9998|0|1|0|0|0|Actor21|0:30020|0|1|0")
            client.sendLine("[O_HERE]|22|0:1|1.5|3.9998|0|1|0|0|0|Actor22|0:30020|0|1|0")
            client.sendLine("[O_HERE]|23|0:1|1.5|4.9998|0|1|0|0|0|Actor23|0:30020|0|1|0")
            client.sendLine("[O_HERE]|24|0:1|2.5|0.9998|0|1|0|0|0|Actor24|0:30020|0|1|0")
            client.sendLine("[O_HERE]|25|0:1|2.5|1.9998|0|1|0|0|0|Actor25|0:30020|0|1|0")
            client.sendLine("[O_HERE]|26|0:1|2.5|2.9998|0|1|0|0|0|Actor26|0:30020|0|1|0")
            client.sendLine("[O_HERE]|27|0:1|2.5|3.9998|0|1|0|0|0|Actor27|0:30020|0|1|0")
            client.sendLine("[O_HERE]|28|0:1|2.5|4.9998|0|1|0|0|0|Actor28|0:30020|0|1|0")
            client.sendLine("[O_HERE]|29|0:1|3.5|0.9998|0|1|0|0|0|Actor29|0:30020|0|1|0")
            client.sendLine("[O_HERE]|30|0:1|3.5|1.9998|0|1|0|0|0|Actor30|0:30020|0|1|0")
            client.sendLine("[O_HERE]|31|0:1|3.5|2.9998|0|1|0|0|0|Actor31|0:30020|0|1|0")
            client.sendLine("[O_HERE]|32|0:1|3.5|3.9998|0|1|0|0|0|Actor32|0:30020|0|1|0")
            client.sendLine("[O_HERE]|33|0:1|3.5|4.9998|0|1|0|0|0|Actor33|0:30020|0|1|0")
            client.sendLine("[O_HERE]|34|0:1|4.5|0.9998|0|1|0|0|0|Actor34|0:30020|0|1|0")
            client.sendLine("[O_HERE]|35|0:1|4.5|1.9998|0|1|0|0|0|Actor35|0:30020|0|1|0")
            client.sendLine("[O_HERE]|36|0:1|4.5|2.9998|0|1|0|0|0|Actor36|0:30020|0|1|0")
            client.sendLine("[O_HERE]|37|0:1|4.5|3.9998|0|1|0|0|0|Actor37|0:30020|0|1|0")
            client.sendLine("[O_HERE]|38|0:1|4.5|4.9998|0|1|0|0|0|Actor38|0:30020|0|1|0")
            client.sendLine("[O_HERE]|39|0:1|5.5|0.9998|0|1|0|0|0|Actor39|0:30020|0|1|0")
            client.sendLine("[O_HERE]|40|0:1|5.5|1.9998|0|1|0|0|0|Actor40|0:30020|0|1|0")
            client.sendLine("[O_HERE]|41|0:1|5.5|2.9998|0|1|0|0|0|Actor41|0:30020|0|1|0")
            client.sendLine("[O_HERE]|42|0:1|5.5|3.9998|0|1|0|0|0|Actor42|0:30020|0|1|0")
            client.sendLine("[O_HERE]|43|0:1|5.5|4.9998|0|1|0|0|0|Actor43|0:30020|0|1|0")
            client.sendLine("[O_HERE]|44|0:1|6.5|0.9998|0|1|0|0|0|Actor44|0:30020|0|1|0")
            client.sendLine("[O_HERE]|45|0:1|6.5|1.9998|0|1|0|0|0|Actor45|0:30020|0|1|0")
            client.sendLine("[O_HERE]|46|0:1|6.5|2.9998|0|1|0|0|0|Actor46|0:30020|0|1|0")
            client.sendLine("[O_HERE]|47|0:1|6.5|3.9998|0|1|0|0|0|Actor47|0:30020|0|1|0")
            client.sendLine("[O_HERE]|48|0:1|6.5|4.9998|0|1|0|0|0|Actor48|0:30020|0|1|0")
            client.sendLine("[O_HERE]|49|0:1|7.5|0.9998|0|1|0|0|0|Actor49|0:30020|0|1|0")
            client.sendLine("[O_HERE]|50|0:1|7.5|1.9998|0|1|0|0|0|Actor50|0:30020|0|1|0")
            client.sendLine("[O_HERE]|51|0:1|7.5|2.9998|0|1|0|0|0|Actor51|0:30020|0|1|0")
            client.sendLine("[O_HERE]|52|0:1|7.5|3.9998|0|1|0|0|0|Actor52|0:30020|0|1|0")
            client.sendLine("[O_HERE]|53|0:1|7.5|4.9998|0|1|0|0|0|Actor53|0:30020|0|1|0")
            client.sendLine("[O_HERE]|54|0:1|8.5|0.9998|0|1|0|0|0|Actor54|0:30020|0|1|0")
            client.sendLine("[O_HERE]|55|0:1|8.5|1.9998|0|1|0|0|0|Actor55|0:30020|0|1|0")
            client.sendLine("[O_HERE]|56|0:1|8.5|2.9998|0|1|0|0|0|Actor56|0:30020|0|1|0")
            client.sendLine("[O_HERE]|57|0:1|8.5|3.9998|0|1|0|0|0|Actor57|0:30020|0|1|0")
            client.sendLine("[O_HERE]|58|0:1|8.5|4.9998|0|1|0|0|0|Actor58|0:30020|0|1|0")
            client.sendLine("[O_HERE]|59|0:100394|2.5|1|0|1|0|0|0|Actor59|0:100145|0|1|0")
            client.sendLine("[O_SPRITE]|59|0:100394|0|")
            client.sendLine("[O_HERE]|60|0:100394|6.5|1|0|1|0|0|0|Actor60|0:100145|0|1|0")
            client.sendLine("[O_SPRITE]|60|0:100394|0|")
            client.sendLine("[O_HERE]|61|0:100394|2.5|5|0|1|0|0|0|Actor61|0:100145|0|1|0")
            client.sendLine("[O_SPRITE]|61|0:100394|0|")
            client.sendLine("[O_HERE]|62|0:100394|6.5|5|0|1|0|0|0|Actor62|0:100145|0|1|0")
            client.sendLine("[O_SPRITE]|62|0:100394|0|")
            client.sendLine("[O_MOVE]|12|0.5|1|128")
            client.sendLine("[P_TILECHANGE]|0|0|4")
            client.sendLine("[O_ANIM]|12|0:100048|loop|800|1|0|12|1|0|0")
            client.sendLine("[O_HERE]|63|0:1|0.5|1.0004|0|1|0|0|0|Actor63|0:30040|0|1|0")
            client.sendLine("[O_SPRITEANIM]|63|1|1|0|play_once|0")
            client.sendLine("[O_SPRITE]|63|0:100395|1|")
            client.sendLine("[O_MOVE]|13|0.5|5|128")
            client.sendLine("[P_TILECHANGE]|0|4|4")
            client.sendLine("[O_ANIM]|13|0:100389|loop|700|1|0|13|2|0|0")
            client.sendLine("[O_HERE]|64|0:1|0.5|5.0004|0|1|0|0|0|Actor64|0:30040|0|1|0")
            client.sendLine("[O_SPRITEANIM]|64|1|1|0|play_once|0")
            client.sendLine("[O_SPRITE]|64|0:100395|1|")
            client.sendLine("[O_MOVE]|4|0.5|3|128")
            client.sendLine("[P_TILECHANGE]|0|2|4")
            client.sendLine("[O_HERE]|1|0:1840007|0|0|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_HERE]|65|0:1|0.5|3.0004|0|1|0|0|0|Actor65|0:30040|0|1|0")
            client.sendLine("[O_SPRITEANIM]|65|1|1|0|play_once|0")
            client.sendLine("[O_SPRITE]|65|0:100395|8|")
            client.sendLine("[O_HERE]|99|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_MOVE]|99|0.5|4|128")
            client.sendLine("[O_ANIM]|99|0:100361|loop|700|1|0|13|2|0|0")
            client.sendLine("[O_HERE]|12|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_HERE]|100|0:1|4.5|2.5|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_MOVE]|100|0.5|1|128")
            client.sendLine("[O_ANIM]|100|0:8740002|loop|700|1|0|13|2|0|0")
            client.sendLine("[O_HERE]|233|0:100300|0|0|0|1|0|0|0||0:1|0|1|0")
            client.sendLine("[O_HERE]|101|0:100063|0.5|1|0|1|0|0|0||0:1|0|1|0")
