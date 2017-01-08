# Panda3D Imports

from direct.actor.Actor import Actor
from pandac.PandaModules import *
from direct.task import Task
import math
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence

# The following line is deprecated:
#import direct.directbase.DirectStart
# And is replaced with:
#from direct.showbase.ShowBase import ShowBase # Already imported, see above
base = ShowBase()
# If you were to run the deprecated line instead,
# The command line would warn,
# "Using deprecated DirectStart interface."
# Before showing the known pipe types etc.
# For more info on deprecation, visit:
# https://www.panda3d.org/manual/index.php/Starting_Panda3D
# Archived on Dec 12 2016 at archive.org.

from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject

# Duplication Import

import copy

# copy.deepcopy(object) to duplicate objects

# Time Import

import time

# time.sleep(seconds) to pause operation



# Loads the model.
#object = loader.loadModel("Models/Black Floor Tile/Black Floor Tile.bam")

# Sets the position.
# Seems to be in X, Y, Z format, but here,
# X is right-left,
# Y is front-back,
# Z is up-down.
# That is, from the camera's perspective in its default position.
#object.setPos(0, 10, 0)

# Sets the rotation.
#object.setHpr(0, 0, 0)

# This sets the scale.
# Setting it to 2 doubles the size,
# Setting it to 0.5 halves the size,
# etc.
#object.setScale(1, 1, 1)

# Renders the model.
# Without the following line of code, the model will not appear at all.
#object.reparentTo(render)

# Hmm...
# The following line of code seems to only crash pview.
# But if it does work,
# The placer panel for this object will pop up,
# Which lets you edit the position, rotation, etc. while the program is running.
# That makes it easier and faster for you to correctly set such attributes.

#object.place()



# Floor Tile Renderer Functions (I'm quite lazy so I made these lol)
# Renders a row of tiles

# Black-and-White Tiles

def render_pattern_tiles(startx=0, starty=0, startz=0, startcolor="black",
                         direction="-x", amount=5):
    black = loader.loadModel("Models/Black Floor Tile/Black Floor Tile.bam")
    white = loader.loadModel("Models/White Floor Tile/White Floor Tile.bam")

    starting_color = startcolor.lower()

    multiplier = 1
    if direction[0] == "-":
        multiplier = -1
    distance = 0.3 * multiplier # 0.3 is twice the "radius" of each tile model
    del multiplier

    tiles_list = []
    place_x = startx
    place_y = starty
    place_z = startz
    current_color = startcolor

    while amount > 0:
        if current_color == "black":
            tiles_list.append(copy.deepcopy(black))
            tiles_list.reverse()
            tiles_list[0].setScale(1, 1, 1)
            tiles_list[0].setPos(place_x, place_y, place_z)
            tiles_list[0].setHpr(0, 0, 0)
            tiles_list[0].reparentTo(render)
            tiles_list.reverse()
            if direction == "x" or direction == "-x":
                place_x += distance
            if direction == "y" or direction == "-y":
                place_y += distance
            if direction == "z" or direction == "-z":
                place_z += distance
            next_color = "white"
            
        if current_color == "white":
            tiles_list.append(copy.deepcopy(white))
            tiles_list.reverse()
            tiles_list[0].setScale(1, 1, 1)
            tiles_list[0].setPos(place_x, place_y, place_z)
            tiles_list[0].setHpr(0, 0, 0)
            tiles_list[0].reparentTo(render)
            tiles_list.reverse()
            if direction == "x" or direction == "-x":
                place_x += distance
            if direction == "y" or direction == "-y":
                place_y += distance
            if direction == "z" or direction == "-z":
                place_z += distance
            next_color = "black"

        current_color = next_color
        del next_color
        amount -= 1

    return tiles_list

# Ivory Tiles

def render_ivory_tiles(startx=0, starty=0, startz=0, direction="-x", amount=5):
    tile_model = loader.loadModel("Models/Ivory Floor Tile/Ivory Floor Tile.bam")

    multiplier = 1
    if direction[0] == "-":
        multiplier = -1
    distance = 0.6 * multiplier # 0.3 is twice the "radius" of each tile model
    del multiplier
    
    tiles_list = []
    place_x = startx
    place_y = starty
    place_z = startz

    while amount > 0:
        tiles_list.append(copy.deepcopy(tile_model))
        tiles_list.reverse()
        tiles_list[0].setScale(1, 1, 1)
        tiles_list[0].setPos(place_x, place_y, place_z)
        tiles_list[0].setHpr(0, 0, 0)
        tiles_list[0].reparentTo(render)
        tiles_list.reverse()
        if direction == "x" or direction == "-x":
            place_x += distance
        if direction == "y" or direction == "-y":
            place_y += distance
        if direction == "z" or direction == "-z":
            place_z += distance
        amount -= 1

    return tiles_list



# Scenes & Keyboard Bindings

# Short Shorts Anims

ShortShortsTorsoAnims = {
                            'TorsoIdle': 'phase_3/models/char/tt_a_chr_dgs_shorts_torso_1000.bam',
                            'TorsoNeutralAnim':'phase_3/models/char/tt_a_chr_dgs_shorts_torso_neutral.bam',
                            'TorsoRunAnim':'phase_3/models/char/tt_a_chr_dgs_shorts_torso_run.bam',
                            
                            'TorsoAngryAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_angry.bam',
                            'TorsoBookAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_book.bam',
                            'TorsoSurprisedAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_conked.bam',
                            'TorsoCringeAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_cringe.bam',
                            'TorsoDuckAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_duck.bam',
                            'TorsoJBRAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump-back-right.bam',
                            'TorsoJZAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump-z.bam',
                            'TorsoJZEAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump-zend.bam',
                            'TorsoJZHAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump-zhang.bam',
                            'TorsoJZSAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump-zstart.bam',
                            'TorsoJumpAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_jump.bam',
                            'TorsoLZAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_leap-z.bam',
                            'TorsoLZEAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_leap-zend.bam',
                            'TorsoLZHAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_leap-zhang.bam',
                            'TorsoLZHLAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_leap-zhanglong.bam',
                            'TorsoLZSAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_leap-zstart.bam',
                            'TorsoPTAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_pie-throw.bam',
                            'TorsoPBAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_press-button.bam',
                            'TorsoRJAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_running-jump.bam',
                            'TorsoShrugAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_shrug.bam',
                            'TorsoSSLAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_sidestep-left.bam',
                            'TorsoTeleportAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_teleport.bam',
                            'TorsoVDAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_victory-dance.bam',
                            'TorsoWalkAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_walk.bam',
                            'TorsoWaveAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_torso_wave.bam',
                
                            'TorsoApplauseAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_applause.bam',
                            'TorsoBCAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_begCycle.bam',
                            'TorsoBOAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_begOut.bam',
                            'TorsoBoredAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_bored.bam',
                            'TorsoBowAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_bow.bam',
                            'TorsoCastAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_cast.bam',
                            'TorsoCLAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_castlong.bam',
                            'TorsoConfusedAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_confused.bam',
                            'TorsoDownAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_down.bam',
                            'TorsoENAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_eat_neutral.bam',
                            'TorsoENRAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_eatnrun.bam',
                            'TorsoFishAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_fish.bam',
                            'TorsoFAAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_fishAGAIN.bam',
                            'TorsoFEAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_fishEND.bam',
                            'TorsoFNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_fishneutral.bam',
                            'TorsoGNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_gameneutral.bam',
                            'TorsoGRAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_gamerun.bam',
                            'TorsoGTAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_gameThrow.bam',
                            'TorsoGiveAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_give.bam',
                            'TorsoIBAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_intoBeg.bam',
                            'TorsoISAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_intoSit.bam',
                            'TorsoLeftAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_left.bam',
                            'TorsoLWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_losewalk.bam',
                            'TorsoPEAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_petend.bam',
                            'TorsoPIAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_petin.bam',
                            'TorsoPLAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_petloop.bam',
                            'TorsoPoleAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_pole.bam',
                            'TorsoPNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_poleneutralbam',
                            'TorsoReelAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_reel.bam',
                            'TorsoRHAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_reelH.bam',
                            'TorsoRNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_reelneutral.bam',
                            'TorsoRightAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_right.bam',
                            'TorsoSNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_sad-neutral.bam',
                            'TorsoSGAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_scientistGame.bam',
                            'TorsoSJAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_scientistJealous.bam',
                            'TorsoSWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_scientistWork.bam',
                            'TorsoSitAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_sit.bam',
                            'TorsoSBAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_slip-backward.bam',
                            'TorsoSFAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_slip-forward.bam',
                            'TorsoSwimAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_swim.bam',
                            'TorsoSwingAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_swing.bam',
                            'TorsoTauntAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_taunt.bam',
                            'TorsoThinkAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_think.bam',
                            'TorsoTOWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_tug-o-war.bam',
                            'TorsoUpAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_torso_up.bam',
                    
                            'TorsoClimbAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_climb.bam',
                            'TorsoHoseAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_firehose.bam',
                            'TorsoDanceAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_happy-dance.bam',
                            'TorsoHoldBottleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_hold-bottle.bam',
                            'TorsoHoldMagnetAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_hold-magnet.bam',
                            'TorsoHypnotizeAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_hypnotize.bam',
                            'TorsoJuggleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_juggle.bam',
                            'TorsoLoseAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_lose.bam',
                            'TorsoMeltAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_melt.bam',
                            'TorsoShoutAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_shout.bam',
                            'TorsoSmoochAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_smooch.bam',
                            'TorsoSpitAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_spit.bam',
                            'TorsoDustAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_sprinkle-dust.bam',
                            'TorsoStruggleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_struggle.bam',
                            'TorsoTickleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_tickle.bam',
                            'TorsoTossAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_toss.bam',
                            'TorsoGunAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_torso_water-gun.bam',
                
                            'TorsoCPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_callPet.bam',
                            'TorsoFPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_feedPet.bam',
                            'TorsoIDAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_into_dig.bam',
                            'TorsoJJAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_jellybeanJar.bam',
                            'TorsoLDAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_loop_dig.bam',
                            'TorsoPBAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_phoneBack.bam',
                            'TorsoPNAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_phoneNeutral.bam',
                            'TorsoTPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_takePhone.bam',
                            'TorsoWaterAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_torso_water.bam',
                
                            'TorsoBPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_bad-putt.bam',
                            'TorsoBLPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_badloop-putt.bam',
                            'TorsoGPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_good-putt.bam',
                            'TorsoHDPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_headdown-putt.bam',
                            'TorsoIPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_into-putt.bam',
                            'TorsoLkPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_look-putt.bam',
                            'TorsoLUPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_lookup-putt.bam',
                            'TorsoLpPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_loop-putt.bam',
                            'TorsoRLPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_rotateL-putt.bam',
                            'TorsoRRPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_rotateR-putt.bam',
                            'TorsoSPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_torso_swing-putt.bam',
                
                            'TorsoBlockAnim':'phase_9/models/char/tt_a_chr_dgs_shorts_torso_block.bam',
                            'TorsoPushAnim':'phase_9/models/char/tt_a_chr_dgs_shorts_torso_push.bam',

                            'TorsoLNAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_torso_leverNeutral.bam',
                            'TorsoLPAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_torso_levelPull.bam',
                            'TorsoLRAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_torso_leverReach.bam'
                        }

ShortShortsLegsAnims = {
                            'LegsIdle':'phase_3/models/char/tt_a_chr_dgs_shorts_legs_1000.bam',
                            'LegsNeutralAnim':'phase_3/models/char/tt_a_chr_dgs_shorts_legs_neutral.bam',
                            'LegsRunAnim':'phase_3/models/char/tt_a_chr_dgs_shorts_legs_run.bam',
                            
                            'LegsAngryAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_angry.bam',
                            'LegsBookAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_book.bam',
                            'LegsSurprisedAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_conked.bam',
                            'LegsCringeAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_cringe.bam',
                            'LegsDuckAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_duck.bam',
                            'LegsJBRAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-back-right.bam',
                            'LegsJZAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-z.bam',
                            'LegsJZEAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zend.bam',
                            'LegsJZHAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zhang.bam',
                            'LegsJZSAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zstart.bam',
                            'LegsJumpAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump.bam',
                            'LegsLZAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap-z.bam',
                            'LegsLZEAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap-zend.bam',
                            'LegsLZHAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap-zhang.bam',
                            'LegsLZHLAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap-zhanglong.bam',
                            'LegsLZSAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap-zstart.bam',
                            'LegsPTAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_pie-throw.bam',
                            'LegsPBAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_press-button.bam',
                            'LegsRJAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_running-jump.bam',
                            'LegsShrugAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_shrug.bam',
                            'LegsSSLAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_sidestep-left.bam',
                            'LegsTeleportAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_teleport.bam',
                            'LegsVDAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_victory-dance.bam',
                            'LegsWalkAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_walk.bam',
                            'LegsWaveAnim':'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_wave.bam',
                
                            'LegsApplauseAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_applause.bam',
                            'LegsBCAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_begCycle.bam',
                            'LegsBOAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_begOut.bam',
                            'LegsBoredAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_bored.bam',
                            'LegsBowAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_bow.bam',
                            'LegsCastAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_cast.bam',
                            'LegsCLAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_castlong.bam',
                            'LegsConfusedAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_confused.bam',
                            'LegsDownAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_down.bam',
                            'LegsENAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_eat_neutral.bam',
                            'LegsENRAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_eatnrun.bam',
                            'LegsFishAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fish.bam',
                            'LegsFAAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishAGAIN.bam',
                            'LegsFEAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishEND.bam',
                            'LegsFNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishneutral.bam',
                            'LegsGNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gameneutral.bam',
                            'LegsGRAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gamerun.bam',
                            'LegsGTAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gameThrow.bam',
                            'LegsGiveAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_give.bam',
                            'LegsIBAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_intoBeg.bam',
                            'LegsISAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_intoSit.bam',
                            'LegsLeftAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_left.bam',
                            'LegsLWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_losewalk.bam',
                            'LegsPEAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petend.bam',
                            'LegsPIAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petin.bam',
                            'LegsPLAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petloop.bam',
                            'LegsPoleAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_pole.bam',
                            'LegsPNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_poleneutralbam',
                            'LegsReelAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reel.bam',
                            'LegsRHAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reelH.bam',
                            'LegsRNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reelneutral.bam',
                            'LegsRightAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_right.bam',
                            'LegsSNAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_sad-neutral.bam',
                            'LegsSGAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistGame.bam',
                            'LegsSJAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistJealous.bam',
                            'LegsSWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistWork.bam',
                            'LegsSitAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_sit.bam',
                            'LegsSBAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_slip-backward.bam',
                            'LegsSFAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_slip-forward.bam',
                            'LegsSwimAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_swim.bam',
                            'LegsSwingAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_swing.bam',
                            'LegsTauntAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_taunt.bam',
                            'LegsThinkAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_think.bam',
                            'LegsTOWAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_tug-o-war.bam',
                            'LegsUpAnim':'phase_4/models/char/tt_a_chr_dgs_shorts_legs_up.bam',
                
                            'LegsClimbAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_climb.bam',
                            'LegsHoseAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_firehose.bam',
                            'LegsDanceAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_happy-dance.bam',
                            'LegsHoldBottleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hold-bottle.bam',
                            'LegsHoldMagnetAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hold-magnet.bam',
                            'LegsHypnotizeAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hypnotize.bam',
                            'LegsJuggleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_juggle.bam',
                            'LegsLoseAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_lose.bam',
                            'LegsMeltAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_melt.bam',
                            'LegsShoutAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_shout.bam',
                            'LegsSmoochAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_smooch.bam',
                            'LegsSpitAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_spit.bam',
                            'LegsDustAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_sprinkle-dust.bam',
                            'LegsStruggleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_struggle.bam',
                            'LegsTickleAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_tickle.bam',
                            'LegsTossAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_toss.bam',
                            'LegsGunAnim':'phase_5/models/char/tt_a_chr_dgs_shorts_legs_water-gun.bam',
                
                            'LegsCPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_callPet.bam',
                            'LegsFPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_feedPet.bam',
                            'LegsIDAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_into_dig.bam',
                            'LegsJJAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_jellybeanJar.bam',
                            'LegsLDAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_loop_dig.bam',
                            'LegsPBAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_phoneBack.bam',
                            'LegsPNAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_phoneNeutral.bam',
                            'LegsTPAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_takePhone.bam',
                            'LegsWaterAnim':'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_water.bam',
                    
                            'LegsBPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_bad-putt.bam',
                            'LegsBLPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_badloop-putt.bam',
                            'LegsGPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_good-putt.bam',
                            'LegsHDPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_headdown-putt.bam',
                            'LegsIPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_into-putt.bam',
                            'LegsLkPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_look-putt.bam',
                            'LegsLUPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_lookup-putt.bam',
                            'LegsLpPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_loop-putt.bam',
                            'LegsRLPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_rotateL-putt.bam',
                            'LegsRRPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_rotateR-putt.bam',
                            'LegsSPAnim':'phase_6/models/char/tt_a_chr_dgs_shorts_legs_swing-putt.bam',

                            'LegsBlockAnim':'phase_9/models/char/tt_a_chr_dgs_shorts_legs_block.bam',
                            'LegsPushAnim':'phase_9/models/char/tt_a_chr_dgs_shorts_legs_push.bam',

                            'LegsLNAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_legs_leverNeutral.bam',
                            'LegsLPAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_legs_levelPull.bam',
                            'LegsLRAnim':'phase_10/models/char/tt_a_chr_dgs_shorts_legs_leverReach.bam'
                        }

# Long Shorts Anims

LongShortsTorsoAnims = {
                            'TorsoIdle': 'phase_3/models/char/tt_a_chr_dgl_shorts_torso_1000.bam',
                            'TorsoNeutralAnim':'phase_3/models/char/tt_a_chr_dgl_shorts_torso_neutral.bam',
                            'TorsoRunAnim':'phase_3/models/char/tt_a_chr_dgl_shorts_torso_run.bam',
                            
                            'TorsoAngryAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_angry.bam',
                            'TorsoBookAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_book.bam',
                            'TorsoSurprisedAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_conked.bam',
                            'TorsoCringeAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_cringe.bam',
                            'TorsoDuckAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_duck.bam',
                            'TorsoJBRAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-back-right.bam',
                            'TorsoJZAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-z.bam',
                            'TorsoJZEAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zend.bam',
                            'TorsoJZHAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zhang.bam',
                            'TorsoJZSAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zstart.bam',
                            'TorsoJumpAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump.bam',
                            'TorsoLZAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap-z.bam',
                            'TorsoLZEAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap-zend.bam',
                            'TorsoLZHAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap-zhang.bam',
                            'TorsoLZHLAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap-zhanglong.bam',
                            'TorsoLZSAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap-zstart.bam',
                            'TorsoPTAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_pie-throw.bam',
                            'TorsoPBAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_press-button.bam',
                            'TorsoRJAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_running-jump.bam',
                            'TorsoShrugAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_shrug.bam',
                            'TorsoSSLAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_sidestep-left.bam',
                            'TorsoTeleportAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_teleport.bam',
                            'TorsoVDAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_victory-dance.bam',
                            'TorsoWalkAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_walk.bam',
                            'TorsoWaveAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_wave.bam',
                
                            'TorsoApplauseAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_applause.bam',
                            'TorsoBCAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_begCycle.bam',
                            'TorsoBOAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_begOut.bam',
                            'TorsoBoredAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_bored.bam',
                            'TorsoBowAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_bow.bam',
                            'TorsoCastAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_cast.bam',
                            'TorsoCLAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_castlong.bam',
                            'TorsoConfusedAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_confused.bam',
                            'TorsoDownAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_down.bam',
                            'TorsoENAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_eat_neutral.bam',
                            'TorsoENRAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_eatnrun.bam',
                            'TorsoFishAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fish.bam',
                            'TorsoFAAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishAGAIN.bam',
                            'TorsoFEAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishEND.bam',
                            'TorsoFNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishneutral.bam',
                            'TorsoGNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gameneutral.bam',
                            'TorsoGRAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gamerun.bam',
                            'TorsoGTAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gameThrow.bam',
                            'TorsoGiveAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_give.bam',
                            'TorsoIBAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_intoBeg.bam',
                            'TorsoISAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_intoSit.bam',
                            'TorsoLeftAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_left.bam',
                            'TorsoLWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_losewalk.bam',
                            'TorsoPEAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petend.bam',
                            'TorsoPIAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petin.bam',
                            'TorsoPLAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petloop.bam',
                            'TorsoPoleAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_pole.bam',
                            'TorsoPNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_poleneutralbam',
                            'TorsoReelAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reel.bam',
                            'TorsoRHAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reelH.bam',
                            'TorsoRNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reelneutral.bam',
                            'TorsoRightAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_right.bam',
                            'TorsoSNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_sad-neutral.bam',
                            'TorsoSGAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistGame.bam',
                            'TorsoSJAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistJealous.bam',
                            'TorsoSWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistWork.bam',
                            'TorsoSitAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_sit.bam',
                            'TorsoSBAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_slip-backward.bam',
                            'TorsoSFAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_slip-forward.bam',
                            'TorsoSwimAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_swim.bam',
                            'TorsoSwingAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_swing.bam',
                            'TorsoTauntAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_taunt.bam',
                            'TorsoThinkAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_think.bam',
                            'TorsoTOWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_tug-o-war.bam',
                            'TorsoUpAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_torso_up.bam',
                    
                            'TorsoClimbAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_climb.bam',
                            'TorsoHoseAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_firehose.bam',
                            'TorsoDanceAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_happy-dance.bam',
                            'TorsoHoldBottleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hold-bottle.bam',
                            'TorsoHoldMagnetAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hold-magnet.bam',
                            'TorsoHypnotizeAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hypnotize.bam',
                            'TorsoJuggleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_juggle.bam',
                            'TorsoLoseAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_lose.bam',
                            'TorsoMeltAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_melt.bam',
                            'TorsoShoutAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_shout.bam',
                            'TorsoSmoochAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_smooch.bam',
                            'TorsoSpitAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_spit.bam',
                            'TorsoDustAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_sprinkle-dust.bam',
                            'TorsoStruggleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_struggle.bam',
                            'TorsoTickleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_tickle.bam',
                            'TorsoTossAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_toss.bam',
                            'TorsoGunAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_torso_water-gun.bam',
                
                            'TorsoCPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_callPet.bam',
                            'TorsoFPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_feedPet.bam',
                            'TorsoIDAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_into_dig.bam',
                            'TorsoJJAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_jellybeanJar.bam',
                            'TorsoLDAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_loop_dig.bam',
                            'TorsoPBAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_phoneBack.bam',
                            'TorsoPNAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_phoneNeutral.bam',
                            'TorsoTPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_takePhone.bam',
                            'TorsoWaterAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_water.bam',
                
                            'TorsoBPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_bad-putt.bam',
                            'TorsoBLPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_badloop-putt.bam',
                            'TorsoGPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_good-putt.bam',
                            'TorsoHDPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_headdown-putt.bam',
                            'TorsoIPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_into-putt.bam',
                            'TorsoLkPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_look-putt.bam',
                            'TorsoLUPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_lookup-putt.bam',
                            'TorsoLpPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_loop-putt.bam',
                            'TorsoRLPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_rotateL-putt.bam',
                            'TorsoRRPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_rotateR-putt.bam',
                            'TorsoSPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_torso_swing-putt.bam',
                
                            'TorsoBlockAnim':'phase_9/models/char/tt_a_chr_dgl_shorts_torso_block.bam',
                            'TorsoPushAnim':'phase_9/models/char/tt_a_chr_dgl_shorts_torso_push.bam',

                            'TorsoLNAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_torso_leverNeutral.bam',
                            'TorsoLPAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_torso_levelPull.bam',
                            'TorsoLRAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_torso_leverReach.bam'
                        }

LongShortsLegsAnims = {
                            'LegsIdle':'phase_3/models/char/tt_a_chr_dgl_shorts_legs_1000.bam',
                            'LegsNeutralAnim':'phase_3/models/char/tt_a_chr_dgl_shorts_legs_neutral.bam',
                            'LegsRunAnim':'phase_3/models/char/tt_a_chr_dgl_shorts_legs_run.bam',
                            
                            'LegsAngryAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_angry.bam',
                            'LegsBookAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_book.bam',
                            'LegsSurprisedAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_conked.bam',
                            'LegsCringeAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_cringe.bam',
                            'LegsDuckAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_duck.bam',
                            'LegsJBRAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump-back-right.bam',
                            'LegsJZAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump-z.bam',
                            'LegsJZEAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump-zend.bam',
                            'LegsJZHAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump-zhang.bam',
                            'LegsJZSAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump-zstart.bam',
                            'LegsJumpAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_jump.bam',
                            'LegsLZAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_leap-z.bam',
                            'LegsLZEAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_leap-zend.bam',
                            'LegsLZHAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_leap-zhang.bam',
                            'LegsLZHLAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_leap-zhanglong.bam',
                            'LegsLZSAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_leap-zstart.bam',
                            'LegsPTAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_pie-throw.bam',
                            'LegsPBAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_press-button.bam',
                            'LegsRJAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_running-jump.bam',
                            'LegsShrugAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_shrug.bam',
                            'LegsSSLAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_sidestep-left.bam',
                            'LegsTeleportAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_teleport.bam',
                            'LegsVDAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_victory-dance.bam',
                            'LegsWalkAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_walk.bam',
                            'LegsWaveAnim':'phase_3.5/models/char/tt_a_chr_dgl_shorts_legs_wave.bam',
                
                            'LegsApplauseAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_applause.bam',
                            'LegsBCAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_begCycle.bam',
                            'LegsBOAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_begOut.bam',
                            'LegsBoredAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_bored.bam',
                            'LegsBowAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_bow.bam',
                            'LegsCastAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_cast.bam',
                            'LegsCLAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_castlong.bam',
                            'LegsConfusedAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_confused.bam',
                            'LegsDownAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_down.bam',
                            'LegsENAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_eat_neutral.bam',
                            'LegsENRAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_eatnrun.bam',
                            'LegsFishAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_fish.bam',
                            'LegsFAAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_fishAGAIN.bam',
                            'LegsFEAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_fishEND.bam',
                            'LegsFNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_fishneutral.bam',
                            'LegsGNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_gameneutral.bam',
                            'LegsGRAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_gamerun.bam',
                            'LegsGTAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_gameThrow.bam',
                            'LegsGiveAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_give.bam',
                            'LegsIBAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_intoBeg.bam',
                            'LegsISAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_intoSit.bam',
                            'LegsLeftAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_left.bam',
                            'LegsLWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_losewalk.bam',
                            'LegsPEAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_petend.bam',
                            'LegsPIAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_petin.bam',
                            'LegsPLAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_petloop.bam',
                            'LegsPoleAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_pole.bam',
                            'LegsPNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_poleneutralbam',
                            'LegsReelAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_reel.bam',
                            'LegsRHAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_reelH.bam',
                            'LegsRNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_reelneutral.bam',
                            'LegsRightAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_right.bam',
                            'LegsSNAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_sad-neutral.bam',
                            'LegsSGAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_scientistGame.bam',
                            'LegsSJAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_scientistJealous.bam',
                            'LegsSWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_scientistWork.bam',
                            'LegsSitAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_sit.bam',
                            'LegsSBAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_slip-backward.bam',
                            'LegsSFAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_slip-forward.bam',
                            'LegsSwimAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_swim.bam',
                            'LegsSwingAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_swing.bam',
                            'LegsTauntAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_taunt.bam',
                            'LegsThinkAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_think.bam',
                            'LegsTOWAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_tug-o-war.bam',
                            'LegsUpAnim':'phase_4/models/char/tt_a_chr_dgl_shorts_legs_up.bam',
                
                            'LegsClimbAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_climb.bam',
                            'LegsHoseAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_firehose.bam',
                            'LegsDanceAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_happy-dance.bam',
                            'LegsHoldBottleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_hold-bottle.bam',
                            'LegsHoldMagnetAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_hold-magnet.bam',
                            'LegsHypnotizeAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_hypnotize.bam',
                            'LegsJuggleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_juggle.bam',
                            'LegsLoseAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_lose.bam',
                            'LegsMeltAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_melt.bam',
                            'LegsShoutAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_shout.bam',
                            'LegsSmoochAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_smooch.bam',
                            'LegsSpitAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_spit.bam',
                            'LegsDustAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_sprinkle-dust.bam',
                            'LegsStruggleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_struggle.bam',
                            'LegsTickleAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_tickle.bam',
                            'LegsTossAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_toss.bam',
                            'LegsGunAnim':'phase_5/models/char/tt_a_chr_dgl_shorts_legs_water-gun.bam',
                
                            'LegsCPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_callPet.bam',
                            'LegsFPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_feedPet.bam',
                            'LegsIDAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_into_dig.bam',
                            'LegsJJAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_jellybeanJar.bam',
                            'LegsLDAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_loop_dig.bam',
                            'LegsPBAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_phoneBack.bam',
                            'LegsPNAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_phoneNeutral.bam',
                            'LegsTPAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_takePhone.bam',
                            'LegsWaterAnim':'phase_5.5/models/char/tt_a_chr_dgl_shorts_legs_water.bam',
                    
                            'LegsBPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_bad-putt.bam',
                            'LegsBLPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_badloop-putt.bam',
                            'LegsGPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_good-putt.bam',
                            'LegsHDPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_headdown-putt.bam',
                            'LegsIPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_into-putt.bam',
                            'LegsLkPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_look-putt.bam',
                            'LegsLUPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_lookup-putt.bam',
                            'LegsLpPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_loop-putt.bam',
                            'LegsRLPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_rotateL-putt.bam',
                            'LegsRRPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_rotateR-putt.bam',
                            'LegsSPAnim':'phase_6/models/char/tt_a_chr_dgl_shorts_legs_swing-putt.bam',

                            'LegsBlockAnim':'phase_9/models/char/tt_a_chr_dgl_shorts_legs_block.bam',
                            'LegsPushAnim':'phase_9/models/char/tt_a_chr_dgl_shorts_legs_push.bam',

                            'LegsLNAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_legs_leverNeutral.bam',
                            'LegsLPAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_legs_levelPull.bam',
                            'LegsLRAnim':'phase_10/models/char/tt_a_chr_dgl_shorts_legs_leverReach.bam'
                        }



def Main_Character_setup(): # Main Character Setup
    # Some duck Main_Character

    # Hooray for C-style :P
    global Main_Character
    Main_Character = Actor(
    
        # Loading the appropriate models for each body part.
        {
            'Torso':'phase_3/models/char/tt_a_chr_dgl_shorts_torso_1000.bam',
            'Legs':'phase_3/models/char/tt_a_chr_dgl_shorts_legs_1000.bam'
        },
    
        # You could use dgs, dgm, or dgl.
        # s means short, m means medium, and l means long.
        # Make sure to be consistent with this.

        # Loading the appropriate animations for each loaded model.
        {
            'Torso':LongShortsTorsoAnims,
            'Legs':LongShortsLegsAnims
        }
    )

    # Attatching the different body parts to form a single Toon.
    Main_Character.attach('Torso', 'Legs', 'joint_hips')
 
    # Animations will be dealt with on the end of the script.

    Main_Character.setPos(1, 5, 0)
    Main_Character.setHpr(180, 0, 0)
    Main_Character.setScale(0.15)
    Main_Character.reparentTo(render)

    # Head

    Head = loader.loadModel('phase_3/models/char/duck-heads-1000.bam')

    # Open the head model itself using pview (not with a script),
    # Then do Shift-L on the Terminal, which "lists the hierarchy".

    # Since all these stuff stack up together (except for Dogs),
    # Hide what you do not want.

    # The Command-L shortcut will list down all of these while the model is open in pview.

    # Head.find('**/(something here)').hide()

    Head.find('**/muzzle-short-surprise').hide()
    Head.find('**/muzzle-short-sad').hide()
    Head.find('**/muzzle-short-smile').hide()
    Head.find('**/muzzle-short-angry').hide()
    Head.find('**/muzzle-short-laugh').hide()

    Head.find('**/muzzle-long-neutral').hide()
    Head.find('**/muzzle-long-surprise').hide()
    Head.find('**/muzzle-long-sad').hide()
    Head.find('**/muzzle-long-smile').hide()
    Head.find('**/muzzle-long-angry').hide()
    Head.find('**/muzzle-long-laugh').hide()

    Head.find('**/head-front-long').hide()
    Head.find('**/head-long').hide()
    #Head.find('**/ears-long').hide()
    Head.find('**/eyes-long').hide()
    Head.find('**/joint_pupilL_long').hide()
    Head.find('**/joint_pupilR_long').hide()

    # Rendering the head and making sure it's above the neck.
    Neck = Main_Character.find('**/def_head')
    Head.reparentTo(Neck)

    # Gloves
    Gloves = Main_Character.find('**/hands')

    # The folloinwg line sets the color.
    # To get the values to be inserted as arguments,
    
    # Convert the hex value to decimal form,
    # Then divide by 255.
    
    # Do that for each one of three parts of the RGB format,
    # Then insert them in there.
    
    # But near-white is good enough for gloves,
    # So leave all three at 0.99.
    Gloves.setColor(0.99, 0.99, 0.99)
 
    # Sleeves

    # Loads the texture.
    Sleeves = loader.loadTexture('Images/Shirt and Sleeve Color.png')

    # Wraps the texture around the 3D model for sleeves.
    Main_Character.find('**/sleeves').setTexture(Sleeves, 1)
 
    # Shirts
    Shirt = loader.loadTexture('Images/Shirt and Sleeve Color.png')
    Main_Character.find('**/torso-top').setTexture(Shirt, 1)
 
    # Shorts
    Shorts = loader.loadTexture('Images/Shorts Color.png')
    Main_Character.find('**/torso-bot').setTexture(Shorts, 1)
 
    # Shoes/Boots
    Shoes = loader.loadTexture('phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellowLL.jpg')

    # Similar to the heads.

    Main_Character.find('**/shoes').hide()

    Main_Character.find('**/boots_short').show()
    Main_Character.find('**/boots_short').setTexture(Shoes, 1)
    Main_Character.find('**/boots_short').setScale(1.1)

    Main_Character.find('**/boots_long').hide()

    # Feet is not a type of shoe.
    # When a Toon wears a shoe, its feet will be hidden.
    Main_Character.find('**/feet').hide()
 
    # Glasses

    Glasses = loader.loadModel('phase_4/models/accessories/tt_m_chr_avt_acc_msk_dorkGlasses.bam')
    Glasses.reparentTo(Head.find('**/head-front-short'))
    Glasses.setZ(0) # was 0.3
    Glasses.setHpr(180, 350.00, 0)
    Glasses.setScale(0.40)

    # Colors

    # Yes, I threw some functions in there,
    # Which will take all the hex values here,
    # Convert them to whatever format they used (already described above),
    # Then apply them to the Toon.
    Forehead_Color = "FFB47E"
    Backhead_Color = "FFB47E"
    Ears_Color = "FFB47E"
    Neck_Color = "FFB47E"
    Arms_Color = "FFB47E"
    Legs_Color = "FFB47E"
    Feet_Color = "FFB47E"

    # Don't touch unless you know what you're doing.
    Head.find('**/head-front-short').setColor(float(int(Forehead_Color[0:2], 16))/255, float(int(Forehead_Color[2:4], 16))/255, float(int(Forehead_Color[4:6], 16))/255, 1.0)
    Head.find('**/head-short').setColor(float(int(Backhead_Color[0:2], 16))/255, float(int(Backhead_Color[2:4], 16))/255, float(int(Backhead_Color[4:6], 16))/255, 1.0)
    #Head.find('**/ears-short').setColor(float(int(Ears_Color[0:2], 16))/255, float(int(Ears_Color[2:4], 16))/255, float(int(Ears_Color[4:6], 16))/255, 1.0)
    Main_Character.find('**/neck').setColor(float(int(Neck_Color[0:2], 16))/255, float(int(Neck_Color[2:4], 16))/255, float(int(Neck_Color[4:6], 16))/255, 1.0)
    Main_Character.find('**/arms').setColor(float(int(Arms_Color[0:2], 16))/255, float(int(Arms_Color[2:4], 16))/255, float(int(Arms_Color[4:6], 16))/255, 1.0)
    Main_Character.find('**/legs').setColor(float(int(Legs_Color[0:2], 16))/255, float(int(Legs_Color[2:4], 16))/255, float(int(Legs_Color[4:6], 16))/255, 1.0)
    Main_Character.find('**/feet').setColor(float(int(Feet_Color[0:2], 16))/255, float(int(Feet_Color[2:4], 16))/255, float(int(Feet_Color[4:6], 16))/255, 1.0)

def room_setup(): # Room Setup
    global Ivory_Wall
    Ivory_Wall = loader.loadModel("Models/Ivory Wall/Ivory Wall.bam")
    Ivory_Wall.setScale(20, 0.05, 1)
    Ivory_Wall.setPos(0, -0.4, 1.5)
    Ivory_Wall.setHpr(0, 0, 0)
    Ivory_Wall.reparentTo(render)

    global room_tiles
    room_tiles = ([

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(-5),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(-4),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(-3),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(-2),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(-1),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(0),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(1),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(2),
                           direction="x"),

        render_ivory_tiles(amount=20, startx=-0.3*20, starty=0.6*(3),
                           direction="x")])

    global MacBook
    MacBook = loader.loadModel("Models/Apple MacBook Pro 15/mpm_F21.bam")
    MacBook.setScale(0.0015, 0.0015, 0.0015)
    MacBook.setPos(0, 1.5, 0.5)
    MacBook.setHpr(0, 90, 0)
    MacBook.reparentTo(render)

    global Table
    Table = loader.loadModel("Models/Table/Table.bam")
    Table.setScale(1, 1, 1)
    Table.setPos(0, 1.5, 0.2)
    Table.setHpr(0, 0, 0)
    Table.reparentTo(render)

    global room_light1, room_light1_nodepath
    room_light1 = PointLight("room_light1")
    room_light1_nodepath = render.attachNewNode(room_light1)
    room_light1_nodepath.setPos(0, 1, 1)
    render.setLight(room_light1_nodepath)

    global room_light2, room_light2_nodepath
    room_light2 = PointLight("room_light2")
    room_light2_nodepath = render.attachNewNode(room_light2)
    room_light2_nodepath.setPos(0, 5, 1)
    render.setLight(room_light2_nodepath)

    global Red_Sofa
    Red_Sofa = loader.loadModel("Models/Red Sofa/Red Sofa.bam")
    Red_Sofa.setScale(1, 1, 1)
    Red_Sofa.setPos(0, -0.7, 0.3)
    Red_Sofa.setHpr(0, 0, 0)
    Red_Sofa.reparentTo(render)

    global room_light3, room_light3_nodepath
    room_light3 = PointLight("room_light3")
    room_light3_nodepath = render.attachNewNode(room_light3)
    room_light3_nodepath.setPos(0, -0.5, 1.5)
    render.setLight(room_light3_nodepath)

    # Outside-Room Fences
    fence_model = loader.loadModel("Models/Brown Fence/Brown Fence.bam")
    global outroom_fences
    outroom_fences = []
    fence_count = 60
    current_x = -10
    while fence_count > 0:
        current_fence = copy.deepcopy(fence_model)
        current_fence.setScale(0.6, 0.6, 0.3)
        current_fence.setPos(current_x, -3.15, 0)
        current_fence.setHpr(0, 0, 0)
        current_fence.reparentTo(render)
        outroom_fences.append(current_fence)
        current_x += 0.3
        fence_count -= 1

    global room_light4, room_light4_nodepath
    room_light4 = PointLight("room_light3")
    room_light4_nodepath = render.attachNewNode(room_light4)
    room_light4_nodepath.setPos(0, -4, 2)
    render.setLight(room_light4_nodepath)

def scene1(): # Reading Messages
    global Main_Character
    
    try:
        Main_Character.cleanup()
    except:
        pass
    
    Main_Character_setup()
    room_cleanup()
    room_setup()

    Main_Character.setPos(0, 0.6, 0.025)
    Main_Character.setHpr(0, 0, 0)

    Main_Character.stop()
    Main_Character.loop("TorsoNeutralAnim")
    Main_Character.loop("LegsNeutralAnim")
    
    try:
        taskMgr.remove("camera2")
    except:
        pass

    def camera1(task):
        base.camera.setPos(1.75, 4, 1)
        base.camera.setHpr(150, 0, 0)
        return Task.cont
    taskMgr.add(camera1, "camera1")

def scene2(): # Surprised
    global Main_Character

    Main_Character.setPos(0, 0.6, 0.025)
    Main_Character.setHpr(0, 0, 0)

    Main_Character.stop()

    torso_surprised = Main_Character.actorInterval("TorsoSurprisedAnim", loop=0)
    torso_neutral = Main_Character.actorInterval("TorsoNeutralAnim", loop=1)
    legs_surprised = Main_Character.actorInterval("LegsSurprisedAnim", loop=0)
    legs_neutral = Main_Character.actorInterval("LegsNeutralAnim", loop=1)

    torso_sequence = Sequence(torso_surprised, torso_neutral)
    legs_sequence = Sequence(legs_surprised, legs_neutral)

    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera1")
    except:
        pass
    
    try:
        taskMgr.remove("camera3")
    except:
        pass

    def camera2(task):
        base.camera.setPos(1.75, 4, 1)
        base.camera.setHpr(150, 0, 0)
        return Task.cont
    taskMgr.add(camera2, "camera2")

def scene3(): # Going Sad
    global Main_Character

    Main_Character.setPos(0, 0.6, 0.025)
    Main_Character.setHpr(0, 0, 0)

    Main_Character.stop()
    
    torsoanim_sadden = Main_Character.actorInterval("TorsoLoseAnim", duration=3, loop=0)
    torso_rotate1 = Main_Character.hprInterval(3, Vec3(180, 0, 0))
    torsoanim_sadwalk1 = Main_Character.actorInterval("TorsoLWAnim", duration=3, loop=1)
    torsoanim_sadwalk2 = Main_Character.actorInterval("TorsoLWAnim", duration=8, loop=1)
    torso_move1 = Main_Character.posInterval(2, Point3(0, 0, 0.025))
    torso_rotate2 = Main_Character.hprInterval(2, Vec3(270, 0, 0))
    torso_move2 = Main_Character.posInterval(4, Point3(3, 0, 0.025))
    
    legsanim_sadden = Main_Character.actorInterval("LegsLoseAnim", duration=3, loop=0)
    legs_rotate1 = Main_Character.hprInterval(3, Vec3(180, 0, 0))
    legsanim_sadwalk1 = Main_Character.actorInterval("LegsLWAnim", duration=3, loop=1)
    legsanim_sadwalk2 = Main_Character.actorInterval("LegsLWAnim", duration=8, loop=1)
    legs_move1 = Main_Character.posInterval(2, Point3(0, 0, 0.025))
    legs_rotate2 = Main_Character.hprInterval(2, Vec3(270, 0, 0))
    legs_move2 = Main_Character.posInterval(4, Point3(3, 0, 0.025))

    torso_sequence1 = Sequence(torsoanim_sadden, torsoanim_sadwalk1, torsoanim_sadwalk2)
    torso_sequence2 = Sequence(torsoanim_sadden, torso_rotate1, torso_move1, torso_rotate2, torso_move2)
    legs_sequence1 = Sequence(legsanim_sadden, legsanim_sadwalk1, legsanim_sadwalk2)
    legs_sequence2 = Sequence(legsanim_sadden, legs_rotate1, legs_move1, legs_rotate2, torso_move2)

    torso_sequence1.start()
    torso_sequence2.start()
    legs_sequence1.start()
    legs_sequence2.start()

    try:
        taskMgr.remove("camera2")
    except:
        pass
    
    try:
        taskMgr.remove("camera4")
    except:
        pass

    def camera3(task):
        base.camera.setPos(1.75, 4, 1)
        base.camera.setHpr(150, 0, 0)
        return Task.cont
    taskMgr.add(camera3, "camera3")

def scene4(): # Outside Room
    global Main_Character

    Main_Character.setPos(4, -1.2, 0.025)
    Main_Character.setHpr(90, 0, 0)

    Main_Character.stop()

    torsoanim_sadwalk = Main_Character.actorInterval("TorsoLWAnim", duration=8, loop=1)
    torso_move1 = Main_Character.posInterval(6, Point3(0, -1.25, 0.025))
    torso_rotate1 = Main_Character.hprInterval(2, Vec3(180, 0, 0))
    torsoanim_neutral = Main_Character.actorInterval("TorsoNeutralAnim", duration=2, loop=1)
    torsoanim_jump = Main_Character.actorInterval("TorsoISAnim", duration=1, loop=0)
    torso_jump = Main_Character.posInterval(1, Point3(0, -1.25, 0.1))
    torsoanim_sit = Main_Character.actorInterval("TorsoSitAnim", duration=5, loop=1)
    torso_sit = Main_Character.posInterval(0.01, Point3(0, -1.25, 0.1))

    legsanim_sadwalk = Main_Character.actorInterval("LegsLWAnim", duration=8, loop=1)
    legs_move1 = Main_Character.posInterval(6, Point3(0, -1.25, 0.025))
    legs_rotate1 = Main_Character.hprInterval(2, Vec3(180, 0, 0))
    legsanim_neutral = Main_Character.actorInterval("LegsNeutralAnim", duration=2, loop=1)
    legsanim_jump = Main_Character.actorInterval("LegsISAnim", duration=1, loop=0)
    legs_jump = Main_Character.posInterval(1, Point3(0, -1.25, 0.15))
    legsanim_sit = Main_Character.actorInterval("LegsSitAnim", duration=5, loop=1)
    legs_sit = Main_Character.posInterval(0.01, Point3(0, -1.25, 0.1))

    torso_sequence1 = Sequence(torsoanim_sadwalk, torsoanim_neutral, torsoanim_jump, torsoanim_sit)
    torso_sequence2 = Sequence(torso_move1, torso_rotate1, torsoanim_neutral, torso_jump, torso_sit)
    legs_sequence1 = Sequence(legsanim_sadwalk, legsanim_neutral, legsanim_jump, legsanim_sit)
    legs_sequence2 = Sequence(legs_move1, legs_rotate1, legsanim_neutral, legs_jump, legs_sit)

    torso_sequence1.start()
    torso_sequence2.start()
    legs_sequence1.start()
    legs_sequence2.start()

    try:
        taskMgr.remove("camera3")
    except:
        pass
    
    try:
        taskMgr.remove("camera5")
    except:
        pass

    def camera4(task):
        base.camera.setPos(-1.75, -4, 1)
        base.camera.setHpr(-30, 0, 0)
        return Task.cont
    taskMgr.add(camera4, "camera4")

def scene5(): # Cry on Sofa
    global Main_Character

    Main_Character.setPos(0, -1.25, 0.1)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_cry = Main_Character.actorInterval("TorsoSNAnim", duration=5, loop=1)

    legsanim_sit = Main_Character.actorInterval("LegsSitAnim", duration=5, loop=1)

    torso_sequence = Sequence(torsoanim_cry)
    legs_sequence = Sequence(legsanim_sit)

    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera4")
    except:
        pass
    
    try:
        taskMgr.remove("camera6")
    except:
        pass

    def camera5(task):
        base.camera.setPos(-1.75, -4, 1)
        base.camera.setHpr(-30, 0, 0)
        return Task.cont
    taskMgr.add(camera5, "camera5")

def scene6(): # Pray
    global Main_Character

    Main_Character.setPos(0, -1.25, 0.1)
    Main_Character.setHpr(180, 0, 0)
    
    Main_Character.stop()

    torsoanim_pray = Main_Character.actorInterval("TorsoBookAnim", loop=0)

    legsanim_sit = Main_Character.actorInterval("LegsSitAnim", duration=5, loop=1)

    torso_sequence = Sequence(torsoanim_pray)
    legs_sequence = Sequence(legsanim_sit)
    
    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera5")
    except:
        pass
    
    try:
        taskMgr.remove("camera7")
    except:
        pass

    def camera6(task):
        base.camera.setPos(-1.75, -4, 1)
        base.camera.setHpr(-30, 0, 0)
        return Task.cont
    taskMgr.add(camera6, "camera6")

def scene7(): # Walk to House Fence
    global Main_Character

    Main_Character.setPos(0, -1.25, 0.1)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_unsit = Main_Character.actorInterval("TorsoNeutralAnim", duration=2, loop=1)
    torsoanim_walk = Main_Character.actorInterval("TorsoWalkAnim", duration=2, loop=1)
    torso_walk = Main_Character.posInterval(2, Point3(0, -3, 0.1))
    torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=20, loop=1)

    legsanim_unsit = Main_Character.actorInterval("LegsNeutralAnim", duration=2, loop=1)
    legsanim_walk = Main_Character.actorInterval("LegsWalkAnim", duration=2, loop=1)
    legs_walk = Main_Character.posInterval(2, Point3(0, -3, 0.1))
    legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    torso_sequence1 = Sequence(torsoanim_unsit, torsoanim_walk, torsoanim_stand)
    torso_sequence2 = Sequence(torsoanim_unsit, torso_walk)
    legs_sequence1 = Sequence(legsanim_unsit, legsanim_walk, legsanim_stand)
    legs_sequence2 = Sequence(legsanim_unsit, legs_walk)

    torso_sequence1.start()
    torso_sequence2.start()
    legs_sequence1.start()
    legs_sequence2.start()

    try:
        taskMgr.remove("camera6")
    except:
        pass
    
    try:
        taskMgr.remove("camera8")
    except:
        pass

    def camera7(task):
        base.camera.setPos(-1.75, -5, 1)
        base.camera.setHpr(-30, 0, 0)
        return Task.cont
    taskMgr.add(camera7, "camera7")

def scene8(): # House Heights
    global Main_Character

    Main_Character.setPos(0, -3, 0.1)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=20, loop=1)

    legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    torso_sequence = Sequence(torsoanim_stand)
    legs_sequence = Sequence(legsanim_stand)

    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera7")
    except:
        pass
    
    try:
        taskMgr.remove("camera9")
    except:
        pass

    def camera8(task):
        base.camera.setPos(1, -2, 2)
        base.camera.setHpr(150, -30, 0)
        return Task.cont
    taskMgr.add(camera8, "camera8")

def scene9(): # Back to Room
    global Main_Character
    
    balcony_cleanup()
    room_cleanup()
    room_setup()

    try:
        Main_Character.stop()
    except NameError:
        Main_Character_setup()

    Main_Character.setPos(0, -2.75, 0.1)
    Main_Character.setHpr(180, 0, 0)

    torsoanim_rotate1 = Main_Character.actorInterval("TorsoWalkAnim", duration=2, loop=1)
    torsoanim_walk1 = Main_Character.actorInterval("TorsoWalkAnim", duration=1, loop=1)
    torsoanim_rotate2 = Main_Character.actorInterval("TorsoWalkAnim", duration=2, loop=1)
    torsoanim_walk2 = Main_Character.actorInterval("TorsoWalkAnim", duration=3, loop=1)

    legsanim_rotate1 = Main_Character.actorInterval("LegsWalkAnim", duration=2, loop=1)
    legsanim_walk1 = Main_Character.actorInterval("LegsWalkAnim", duration=1, loop=1)
    legsanim_rotate2 = Main_Character.actorInterval("LegsWalkAnim", duration=2, loop=1)
    legsanim_walk2 = Main_Character.actorInterval("LegsWalkAnim", duration=3, loop=1)

    rotate1 = Main_Character.hprInterval(2, Vec3(0, 0, 0))
    walk1 = Main_Character.posInterval(1, Point3(0, -2, 0))
    rotate2 = Main_Character.hprInterval(2, Vec3(-90, 0, 0))
    walk2 = Main_Character.posInterval(3, Point3(3.25, -2, 0))

    torso_sequence = Sequence(torsoanim_rotate1, torsoanim_walk1, torsoanim_rotate2, torsoanim_walk2)
    legs_sequence = Sequence(legsanim_rotate1, legsanim_walk1, legsanim_rotate2, legsanim_walk2)
    movement_sequence = Sequence(rotate1, walk1, rotate2, walk2)

    torso_sequence.start()
    legs_sequence.start()
    movement_sequence.start()

    try:
        taskMgr.remove("camera8")
    except:
        pass
    
    try:
        taskMgr.remove("camera10")
    except:
        pass

    def camera9(task):
        base.camera.setPos(3, -0.5, 1)
        base.camera.setHpr(135, 0, 0)
        return Task.cont
    taskMgr.add(camera9, "camera9")

def room_cleanup(): # Room Cleanup
    print "RC inst"
    
    global Ivory_Wall
    try:
        Ivory_Wall.removeNode()
        del Ivory_Wall
    except NameError:
        print "RC IW NameError"

    global room_tiles
    try:
        for tile_list in room_tiles:
            for floor_tile in tile_list:
                floor_tile.removeNode()
        del room_tiles
    except NameError:
        print "RC RT NameError"

    global MacBook
    try:
        MacBook.removeNode()
        del MacBook
    except NameError:
        print "RC MB NameError"

    global Table
    try:
        Table.removeNode()
        del Table
    except NameError:
        print "RC Table NameError"

    global room_light1, room_light1_nodepath
    try:
        render.clearLight(room_light1_nodepath)
        room_light1_nodepath.removeNode()
        del room_light1, room_light1_nodepath
    except NameError:
        print "RC RL1 NameError"

    global room_light2, room_light2_nodepath
    try:
        render.clearLight(room_light2_nodepath)
        room_light2_nodepath.removeNode()
        del room_light2, room_light2_nodepath
    except NameError:
        print "RC RL2 NameError"

    global Red_Sofa
    try:
        Red_Sofa.removeNode()
        del Red_Sofa
    except NameError:
        print "RC Red_Sofa NameError"

    global room_light3, room_light3_nodepath
    try:
        render.clearLight(room_light3_nodepath)
        room_light3_nodepath.removeNode()
        del room_light3, room_light3_nodepath
    except NameError:
        print "RC RL3 NameError"

    # Outside-Room Fences
    global outroom_fences
    try:
        for fence in outroom_fences:
            fence.removeNode()
        del outroom_fences
    except NameError:
        print "BC ORF NameError"

    global room_light4, room_light4_nodepath
    try:
        render.clearLight(room_light4_nodepath)
        room_light4_nodepath.removeNode()
        del room_light4, room_light4_nodepath
    except NameError:
        print "RC RL4 NameError"

def balcony_setup(): # Balcony Setup
    
    # Floor Tiles Part 1: Balcony

    global balcony_tiles
    balcony_tiles = ([render_pattern_tiles(startx=0.3*(10-1),
                                           starty=3+(0.3*(1-1)),
                                           direction="-x", amount=10),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(2-1)), direction="-x",
                         amount=10, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(3-1)), direction="-x",
                         amount=10),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(4-1)), direction="-x",
                         amount=10, startcolor="white"),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(5-1)), direction="-x",
                         amount=10),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(6-1)), direction="-x",
                         amount=10, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(7-1)), direction="-x",
                         amount=10),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(8-1)), direction="-x",
                         amount=10, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(9-1)), direction="-x",
                         amount=10),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(10-1)), direction="-x",
                         amount=10, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(11-1)), direction="-x",
                         amount=10),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(12-1)), direction="-x",
                         amount=10, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(13-1)), direction="-x",
                         amount=10),

    # floor Tiles Part 2: Lift-Balcony

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(14-1)), direction="-x",
                         amount=10+8+3, startcolor="white"),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(15-1)), direction="-x",
                         amount=10+8+3),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(16-1)), direction="-x",
                         amount=10+8+3, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(17-1)), direction="-x",
                         amount=10+8+3),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(18-1)), direction="-x",
                         amount=10+8+3, startcolor="white"),
    
    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(19-1)), direction="-x",
                         amount=10+8+3),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(20-1)), direction="-x",
                         amount=10+8+3, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(21-1)), direction="-x",
                         amount=10+8+3),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(22-1)), direction="-x",
                         amount=10+8+3, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(23-1)), direction="-x",
                         amount=10+8+3),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(24-1)), direction="-x",
                         amount=10+8, startcolor="white"),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(25-1)), direction="-x",
                         amount=10+8),

    render_pattern_tiles(startx=0.3*(10-1), starty=3+(0.3*(26-1)), direction="-x",
                         amount=10+8, startcolor="white"),

    # Floor Tiles Part 3: Stair-ITL

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(27-1)), direction="-x",
                         amount=8+3),

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(28-1)), direction="-x",
                         amount=8+3, startcolor="white"),

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(29-1)), direction="-x",
                         amount=8+3),

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(30-1)), direction="-x",
                         amount=8+3, startcolor="white"),

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(31-1)), direction="-x",
                         amount=8+3),

    render_pattern_tiles(startx=-0.3, starty=3+(0.3*(32-1)), direction="-x",
                         amount=8+3, startcolor="white")])

    # Lift Cube

    global Lift_Cube
    Lift_Cube = loader.loadModel("Models/Lift Cube/Lift Cube.bam")
    Lift_Cube.setScale(1, 1, 1)
    Lift_Cube.setPos(-1.8, 4.8, 1.5)
    Lift_Cube.setHpr(90, 0, 0)
    Lift_Cube.reparentTo(render)

    # Art Class Wall

    global Art_Wall
    Art_Wall = loader.loadModel("Models/Blue Wall/Blue Wall.bam")
    Art_Wall.setScale(0.05, 7.8, 1)
    Art_Wall.setPos(2.85, 6.75, 1.5)
    Art_Wall.setHpr(0, 0, 0)
    Art_Wall.reparentTo(render)

    # ITL Class Wall

    global ITL_Wall
    ITL_Wall = loader.loadModel("Models/Blue Wall/Blue Wall.bam")
    ITL_Wall.setScale(0.05, 3, 1)
    ITL_Wall.setPos(-3.49, 8.25, 1.5)
    ITL_Wall.setHpr(0, 0, 0)
    ITL_Wall.reparentTo(render)

    # Stair-Balcony Wall

    global SB_Wall
    SB_Wall = loader.loadModel("Models/White Wall/White Wall.bam")
    SB_Wall.setScale(3, 0.05, 1)
    SB_Wall.setPos(1.35, 10.7, 1.5)
    SB_Wall.setHpr(0, 0, 0)
    SB_Wall.reparentTo(render)

    # ITL Pillar

    global ITL_Pillar
    ITL_Pillar = loader.loadModel("Models/White Pillar/White Pillar.bam")
    ITL_Pillar.setScale(0.9, 0.9, 1)
    ITL_Pillar.setPos(-3, 10.2, 1.5)
    ITL_Pillar.setHpr(0, 0, 0)
    ITL_Pillar.reparentTo(render)
    
    # Lighting
    
    global balcony_light1, balcony_light1_nodepath
    balcony_light1 = PointLight("balcony_light1")
    balcony_light1_nodepath = render.attachNewNode(balcony_light1)
    balcony_light1_nodepath.setPos(0, 10, 10)
    render.setLight(balcony_light1_nodepath)

    global balcony_light2, balcony_light2_nodepath
    balcony_light2 = PointLight("balcony_light2")
    balcony_light2_nodepath = render.attachNewNode(balcony_light2)
    balcony_light2_nodepath.setPos(0, 10, -10)
    render.setLight(balcony_light2_nodepath)

    global balcony_light3, balcony_light3_nodepath
    balcony_light3 = PointLight("balcony_light3")
    balcony_light3_nodepath = render.attachNewNode(balcony_light3)
    balcony_light3_nodepath.setPos(0, 4, 1)
    render.setLight(balcony_light3_nodepath)

    # Fences

    fence_model = loader.loadModel("Models/Grey Fence/Grey Fence.bam")
    global balcony_fences
    balcony_fences = []
    fence_count = 10
    current_x = 0
    while fence_count > 0:
        current_fence = copy.deepcopy(fence_model)
        current_fence.setScale(0.6, 0.6, 0.3)
        current_fence.setPos(current_x, 3, 0)
        current_fence.setHpr(0, 0, 0)
        current_fence.reparentTo(render)
        balcony_fences.append(current_fence)
        current_x += 0.3
        fence_count -= 1

    # Fog

    global grey_fog
    grey_fog = Fog("grey_fog")
    grey_fog.setColor(0.05, 0.05, 0.05)
    grey_fog.setExpDensity(0.2)
    render.setFog(grey_fog)
    base.setBackgroundColor(0.2, 0.2, 0.2)

def scene10(): # Sad to Balcony
    global Main_Character
    
    room_cleanup()
    balcony_cleanup()
    balcony_setup()

    try:
        Main_Character.stop()
    except NameError:
        Main_Character_setup()

    Main_Character.setPos(-1.5, 9, 0)
    Main_Character.setHpr(270, 0, 0)

    torsoanim_sadwalk = Main_Character.actorInterval("TorsoLWAnim", duration=14, loop=1)
    torso_move1 = Main_Character.posInterval(4, Point3(1.2, 9, 0))
    torso_rotate1 = Main_Character.hprInterval(2, Vec3(180, 0, 0))
    torso_move2 = Main_Character.posInterval(8, Point3(1.2, 3.6, 0))
    torso_neutral = Main_Character.actorInterval("TorsoNeutralAnim", duration=20, loop=1)

    legsanim_sadwalk = Main_Character.actorInterval("LegsLWAnim", duration=14, loop=1)
    legs_move1 = Main_Character.posInterval(4, Point3(1.2, 9, 0))
    legs_rotate1 = Main_Character.hprInterval(2, Vec3(180, 0, 0))
    legs_move2 = Main_Character.posInterval(8, Point3(1.2, 3.6, 0))
    legs_neutral = Main_Character.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    torso_sequence1 = Sequence(torsoanim_sadwalk)
    torso_sequence2 = Sequence(torso_move1, torso_rotate1, torso_move2, torso_neutral)
    legs_sequence1 = Sequence(legsanim_sadwalk)
    legs_sequence2 = Sequence(legs_move1, legs_rotate1, torso_move2, legs_neutral)

    torso_sequence1.start()
    torso_sequence2.start()
    legs_sequence1.start()
    legs_sequence2.start()
    
    try:
        taskMgr.remove("camera9")
    except:
        pass
    
    try:
        taskMgr.remove("camera11")
    except:
        pass

    def camera10(task):
        base.camera.setPos(0.5, 0, 3)
        base.camera.setHpr(0, -30, 0)
        return Task.cont
    taskMgr.add(camera10, "camera10")

def scene11(): # Balcony Heights
    global Main_Character
    
    Main_Character.setPos(1.2, 3.6, 0)
    Main_Character.setHpr(180, 0, 0)
    
    Main_Character.stop()

    torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=20, loop=1)

    legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    torso_sequence = Sequence(torsoanim_stand)
    legs_sequence = Sequence(legsanim_stand)

    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera10")
    except:
        pass
    
    try:
        taskMgr.remove("camera12")
    except:
        pass

    def camera11(task):
        base.camera.setPos(2.25, 5, 3)
        base.camera.setHpr(165, -45, 0)
        return Task.cont
    taskMgr.add(camera11, "camera11")

def scene12(): # Fence Step
    global Main_Character

    Main_Character.setPos(1.2, 3.6, 0)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_step = Main_Character.actorInterval("TorsoWalkAnim", duration=1, loop=1)
    torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=0.01)

    legsanim_step = Main_Character.actorInterval("LegsWalkAnim", duration=1, loop=1)
    legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=0.01)

    movement_step = Main_Character.posInterval(1, Point3(1.2, 3.1, 0.05))

    torso_sequence = Sequence(torsoanim_step, torsoanim_stand)
    legs_sequence = Sequence(legsanim_step, legsanim_stand)
    movement_sequence = Sequence(movement_step)

    torso_sequence.start()
    legs_sequence.start()
    movement_sequence.start()

    try:
        taskMgr.remove("camera11")
    except:
        pass
    
    try:
        taskMgr.remove("camera13")
    except:
        pass

    def camera12(task):
        base.camera.setPos(2, 4.5, 0.5)
        base.camera.setHpr(150, 0, 0)
        return Task.cont
    taskMgr.add(camera12, "camera12")

def scene13(): # Bell
    global Main_Character

    Main_Character.setPos(1.2, 3.15, 0.05)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=20, loop=1)

    legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    torso_sequence = Sequence(torsoanim_stand)
    legs_sequence = Sequence(legsanim_stand)

    torso_sequence.start()
    legs_sequence.start()

    try:
        taskMgr.remove("camera12")
    except:
        pass
    
    try:
        taskMgr.remove("camera14")
    except:
        pass

    def camera13(task):
        base.camera.setPos(0.5, 0, 3)
        base.camera.setHpr(0, -30, 0)
        return Task.cont
    taskMgr.add(camera13, "camera13")

def scene14(): # Alone to Class
    global Main_Character
    global Friend

    try:
        Friend.cleanup()
    except NameError:
        pass

    Main_Character.setPos(1.2, 3.15, 0.05)
    Main_Character.setHpr(180, 0, 0)

    Main_Character.stop()

    torsoanim_walk = Main_Character.actorInterval("TorsoWalkAnim", duration=14.4, loop=1)

    legsanim_walk = Main_Character.actorInterval("LegsWalkAnim", duration=14.4, loop=1)

    movement_rotate1 = Main_Character.hprInterval(2, Vec3(0, 0, 0))
    movement_walk1 = Main_Character.posInterval(8, Point3(1.2, 9, 0))
    movement_rotate2 = Main_Character.hprInterval(2, Vec3(90, 0, 0))
    movement_walk2 = Main_Character.posInterval(2.4, Point3(-0.9, 9, 0))

    torso_sequence = Sequence(torsoanim_walk)
    legs_sequence = Sequence(legsanim_walk)
    movement_sequence = Sequence(movement_rotate1, movement_walk1, movement_rotate2, movement_walk2)

    torso_sequence.start()
    legs_sequence.start()
    movement_sequence.start()
    
    try:
        taskMgr.remove("camera13")
    except:
        pass
    
    try:
        taskMgr.remove("camera15")
    except:
        pass

    def camera14(task):
        base.camera.setPos(2, 11, 1)
        base.camera.setHpr(160, 0, 0)
        return Task.cont
    taskMgr.add(camera14, "camera14")

def Friend_setup(): # Friend Setup
    # Some mouse friend

    # Hooray for C-style :P
    global Friend
    Friend = Actor(
    
        # Loading the appropriate models for each body part.
        {
            'Torso':'phase_3/models/char/tt_a_chr_dgs_shorts_torso_1000.bam',
            'Legs':'phase_3/models/char/tt_a_chr_dgs_shorts_legs_1000.bam'
        },
    
        # You could use dgs, dgm, or dgl.
        # s means short, m means medium, and l means long.
        # Make sure to be consistent with this.

        # Loading the appropriate animations for each loaded model.
        {
            'Torso':ShortShortsTorsoAnims,
            'Legs':ShortShortsLegsAnims
        }
    )

    # Attatching the different body parts to form a single Toon.
    Friend.attach('Torso', 'Legs', 'joint_hips')
 
    # Animations will be dealt with on the end of the script.

    Friend.setPos(0, 0, 5)
    Friend.setHpr(180, 0, 0)
    Friend.setScale(0.15)
    Friend.reparentTo(render)

    # Head

    Head = loader.loadModel('phase_3/models/char/mouse-heads-1000.bam')

    # Open the head model itself using pview (not with a script),
    # Then do Shift-L on the Terminal, which "lists the hierarchy".

    # Since all these stuff stack up together (except for Dogs),
    # Hide what you do not want.

    # The Command-L shortcut will list down all of these while the model is open in pview.

    # Head.find('**/(something here)').hide()

    Head.find('**/muzzle-short-surprise').hide()
    Head.find('**/muzzle-short-sad').hide()
    Head.find('**/muzzle-short-smile').hide()
    Head.find('**/muzzle-short-angry').hide()
    Head.find('**/muzzle-short-laugh').hide()

    #Head.find('**/muzzle-long-neutral').hide()
    #Head.find('**/muzzle-long-surprise').hide()
    #Head.find('**/muzzle-long-sad').hide()
    #Head.find('**/muzzle-long-smile').hide()
    #Head.find('**/muzzle-long-angry').hide()
    #Head.find('**/muzzle-long-laugh').hide()

    Head.find('**/head-front-long').hide()
    Head.find('**/head-long').hide()
    Head.find('**/ears-long').hide()
    Head.find('**/eyes-long').hide()
    Head.find('**/joint_pupilL_long').hide()
    Head.find('**/joint_pupilR_long').hide()

    # Rendering the head and making sure it's above the neck.
    Neck = Friend.find('**/def_head')
    Head.reparentTo(Neck)

    # Gloves
    Gloves = Friend.find('**/hands')

    # The folloinwg line sets the color.
    # To get the values to be inserted as arguments,
    
    # Convert the hex value to decimal form,
    # Then divide by 255.
    
    # Do that for each one of three parts of the RGB format,
    # Then insert them in there.
    
    # But near-white is good enough for gloves,
    # So leave all three at 0.99.
    Gloves.setColor(0.99, 0.99, 0.99)
 
    # Sleeves

    # Loads the texture.
    Sleeves = loader.loadTexture('Images/Shirt and Sleeve Color.png')

    # Wraps the texture around the 3D model for sleeves.
    Friend.find('**/sleeves').setTexture(Sleeves, 1)
 
    # Shirts
    Shirt = loader.loadTexture('Images/Shirt and Sleeve Color.png')
    Friend.find('**/torso-top').setTexture(Shirt, 1)
 
    # Shorts
    Shorts = loader.loadTexture('Images/Shorts Color.png')
    Friend.find('**/torso-bot').setTexture(Shorts, 1)
 
    # Shoes/Boots
    Shoes = loader.loadTexture('phase_4/maps/icerink.jpg')
    #Shoes = loader.loadTexture('phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellowLL.jpg')

    # Similar to the heads.

    Friend.find('**/shoes').hide()

    Friend.find('**/boots_short').show()
    Friend.find('**/boots_short').setTexture(Shoes, 1)
    Friend.find('**/boots_short').setScale(1.1)

    Friend.find('**/boots_long').hide()

    # Feet is not a type of shoe.
    # When a Toon wears a shoe, its feet will be hidden.
    Friend.find('**/feet').hide()

    # Colors

    # Yes, I threw some functions in there,
    # Which will take all the hex values here,
    # Convert them to whatever format they used (already described above),
    # Then apply them to the Toon.
    Forehead_Color = "FFB47E"
    Backhead_Color = "FFB47E"
    Ears_Color = "FFB47E"
    Neck_Color = "FFB47E"
    Arms_Color = "FFB47E"
    Legs_Color = "FFB47E"
    Feet_Color = "FFB47E"

    # Don't touch unless you know what you're doing.
    Head.find('**/head-front-short').setColor(float(int(Forehead_Color[0:2], 16))/255, float(int(Forehead_Color[2:4], 16))/255, float(int(Forehead_Color[4:6], 16))/255, 1.0)
    Head.find('**/head-short').setColor(float(int(Backhead_Color[0:2], 16))/255, float(int(Backhead_Color[2:4], 16))/255, float(int(Backhead_Color[4:6], 16))/255, 1.0)
    Head.find('**/ears-short').setColor(float(int(Ears_Color[0:2], 16))/255, float(int(Ears_Color[2:4], 16))/255, float(int(Ears_Color[4:6], 16))/255, 1.0)
    Friend.find('**/neck').setColor(float(int(Neck_Color[0:2], 16))/255, float(int(Neck_Color[2:4], 16))/255, float(int(Neck_Color[4:6], 16))/255, 1.0)
    Friend.find('**/arms').setColor(float(int(Arms_Color[0:2], 16))/255, float(int(Arms_Color[2:4], 16))/255, float(int(Arms_Color[4:6], 16))/255, 1.0)
    Friend.find('**/legs').setColor(float(int(Legs_Color[0:2], 16))/255, float(int(Legs_Color[2:4], 16))/255, float(int(Legs_Color[4:6], 16))/255, 1.0)
    Friend.find('**/feet').setColor(float(int(Feet_Color[0:2], 16))/255, float(int(Feet_Color[2:4], 16))/255, float(int(Feet_Color[4:6], 16))/255, 1.0)

def scene15(): # Return to Balcony, Friend Approach
    global Main_Character
    global Friend
    
    Main_Character.stop()
    try:
        Friend.stop()
    except NameError or AssertionError:
        Friend_setup()

    Main_Character.setPos(-1.5, 9, 0)
    Main_Character.setHpr(270, 0, 0)
    Friend.setPos(-0.9, 10, 0)
    Friend.setHpr(210, 0, 0)

    main_torsoanim_sadwalk = Main_Character.actorInterval("TorsoLWAnim", duration=10, loop=1)
    main_torsoanim_sadstand = Main_Character.actorInterval("TorsoSNAnim", duration=20, loop=1)
    
    main_legsanim_sadwalk = Main_Character.actorInterval("LegsLWAnim", duration=10, loop=1)
    main_legsanim_sadstand = Main_Character.actorInterval("LegsSNAnim", duration=20, loop=1)

    main_movement_walk1 = Main_Character.posInterval(4, Point3(1.2, 9, 0))
    main_movement_rotate1 = Main_Character.hprInterval(2, Vec3(180, 0, 0))
    main_movement_walk2 = Main_Character.posInterval(4, Point3(1.2, 6.3, 0))
    
    friend_torsoanim_wait = Friend.actorInterval("TorsoNeutralAnim", duration=6, loop=1)
    friend_torsoanim_run = Friend.actorInterval("TorsoRunAnim", duration=4, loop=1)
    friend_torsoanim_stand = Friend.actorInterval("TorsoNeutralAnim", duration=20, loop=1)
    
    friend_legsanim_wait = Friend.actorInterval("LegsNeutralAnim", duration=6, loop=1)
    friend_legsanim_run = Friend.actorInterval("LegsRunAnim", duration=4, loop=1)
    friend_legsanim_stand = Friend.actorInterval("LegsNeutralAnim", duration=20, loop=1)

    friend_movement_stay = Friend.posInterval(6, Point3(-0.9, 10, 0))
    friend_movement_run = Friend.posInterval(4, Point3(0.9, 6.9, 0))

    main_torso_sequence = Sequence(main_torsoanim_sadwalk, main_torsoanim_sadstand)
    main_legs_sequence = Sequence(main_legsanim_sadwalk, main_legsanim_sadstand)
    main_movement_sequence = Sequence(main_movement_walk1, main_movement_rotate1, main_movement_walk2)
    
    friend_torso_sequence = Sequence(friend_torsoanim_wait, friend_torsoanim_run, friend_torsoanim_stand)
    friend_legs_sequence = Sequence(friend_legsanim_wait, friend_legsanim_run, friend_legsanim_stand)
    friend_movement_sequence = Sequence(friend_movement_stay, friend_movement_run)

    main_torso_sequence.start()
    main_legs_sequence.start()
    main_movement_sequence.start()

    friend_torso_sequence.start()
    friend_legs_sequence.start()
    friend_movement_sequence.start()

    try:
        taskMgr.remove("camera14")
    except:
        pass
    
    try:
        taskMgr.remove("camera16")
    except:
        pass

    def camera15(task):
        base.camera.setPos(0.5, 0, 3)
        base.camera.setHpr(0, -30, 0)
        return Task.cont
    taskMgr.add(camera15, "camera15")

def scene16(): # Rotate to See Friend
    global Main_Character
    global Friend

    Main_Character.stop()
    Friend.stop()

    Main_Character.setPos(1.2, 6.3, 0)
    Main_Character.setHpr(180, 0, 0)
    Friend.setPos(0.9, 6.9, 0)
    Friend.setHpr(210, 0, 0)

    main_torsoanim_raise = Main_Character.actorInterval("TorsoNeutralAnim", duration=2, loop=1)
    main_torsoanim_rotate = Main_Character.actorInterval("TorsoWalkAnim", duration=2, loop=1)
    main_torsoanim_stare = Main_Character.actorInterval("TorsoNeutralAnim", duration=26, loop=1)

    main_legsanim_raise = Main_Character.actorInterval("LegsNeutralAnim", duration=2, loop=1)
    main_legsanim_rotate = Main_Character.actorInterval("LegsWalkAnim", duration=2, loop=1)
    main_legsanim_stare = Main_Character.actorInterval("LegsNeutralAnim", duration=26, loop=1)

    main_movement_stay = Main_Character.posInterval(2, Point3(1.2, 6.3, 0))
    main_movement_rotate = Main_Character.hprInterval(2, Vec3(26.565, 0, 0)) # Approximation of arctan(1/2)

    friend_torsoanim_stand = Friend.actorInterval("TorsoNeutralAnim", duration=30, loop=1)
    friend_legsanim_stand = Friend.actorInterval("LegsNeutralAnim", duration=30, loop=1)

    main_torso_sequence = Sequence(main_torsoanim_raise, main_torsoanim_rotate, main_torsoanim_stare)
    main_legs_sequence = Sequence(main_legsanim_raise, main_legsanim_rotate, main_legsanim_stare)
    main_movement_sequence = Sequence(main_movement_stay, main_movement_rotate)

    friend_torso_sequence = Sequence(friend_torsoanim_stand)
    friend_legs_sequence = Sequence(friend_legsanim_stand)

    main_torso_sequence.start()
    main_legs_sequence.start()
    main_movement_sequence.start()

    friend_torso_sequence.start()
    friend_legs_sequence.start()

    try:
        taskMgr.remove("camera15")
    except:
        pass
    
    try:
        taskMgr.remove("camera17")
    except:
        pass

    def camera16(task):
        base.camera.setPos(0.5, 4, 3)
        base.camera.setHpr(0, -45, 0)
        return Task.cont
    taskMgr.add(camera16, "camera16")

def scene17(): # Conversation-Friend
    global Main_Character
    global Friend

    Main_Character.stop()
    Friend.stop()

    Main_Character.setPos(1.2, 6.3, 0)
    Main_Character.setHpr(26.565, 0, 0)
    Friend.setPos(0.9, 6.9, 0)
    Friend.setHpr(210, 0, 0)

    main_torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=30, loop=1)
    main_legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=30, loop=1)

    friend_torsoanim_stand = Friend.actorInterval("TorsoNeutralAnim", duration=30, loop=1)
    friend_legsanim_stand = Friend.actorInterval("LegsNeutralAnim", duration=30, loop=1)

    main_torso_sequence = Sequence(main_torsoanim_stand)
    main_legs_sequence = Sequence(main_legsanim_stand)
    
    friend_torso_sequence = Sequence(friend_torsoanim_stand)
    friend_legs_sequence = Sequence(friend_legsanim_stand)

    main_torso_sequence.start()
    main_legs_sequence.start()

    friend_torso_sequence.start()
    friend_legs_sequence.start()

    try:
        taskMgr.remove("camera16")
    except:
        pass
    
    try:
        taskMgr.remove("camera18")
    except:
        pass

    def camera17(task):
        base.camera.setPos(1.5, 5, 2)
        base.camera.setHpr(30, -35, 0)
        return Task.cont
    taskMgr.add(camera17, "camera17")

def scene18(): # Conversation-Main_Character
    global Main_Character
    global Friend

    Main_Character.stop()
    Friend.stop()

    Main_Character.setPos(1.2, 6.3, 0)
    Main_Character.setHpr(26.565, 0, 0)
    Friend.setPos(0.9, 6.9, 0)
    Friend.setHpr(210, 0, 0)

    main_torsoanim_stand = Main_Character.actorInterval("TorsoNeutralAnim", duration=30, loop=1)
    main_legsanim_stand = Main_Character.actorInterval("LegsNeutralAnim", duration=30, loop=1)

    friend_torsoanim_stand = Friend.actorInterval("TorsoNeutralAnim", duration=30, loop=1)
    friend_legsanim_stand = Friend.actorInterval("LegsNeutralAnim", duration=30, loop=1)

    main_torso_sequence = Sequence(main_torsoanim_stand)
    main_legs_sequence = Sequence(main_legsanim_stand)
    
    friend_torso_sequence = Sequence(friend_torsoanim_stand)
    friend_legs_sequence = Sequence(friend_legsanim_stand)

    main_torso_sequence.start()
    main_legs_sequence.start()

    friend_torso_sequence.start()
    friend_legs_sequence.start()

    try:
        taskMgr.remove("camera17")
    except:
        pass
    
    try:
        taskMgr.remove("camera19")
    except:
        pass

    def camera18(task):
        base.camera.setPos(1.5, 9, 1)
        base.camera.setHpr(160, 0, 0)
        return Task.cont
    taskMgr.add(camera18, "camera18")

def scene19(): # Together to Class
    global Main_Character
    global Friend

    Main_Character.stop()
    Friend.stop()

    Main_Character.setPos(1.2, 6.3, 0)
    Main_Character.setHpr(26.565, 0, 0)
    Friend.setPos(0.9, 6.9, 0)
    Friend.setHpr(210, 0, 0)
    
    main_torsoanim_wait = Main_Character.actorInterval("TorsoNeutralAnim", duration=2, loop=1)
    main_torsoanim_run = Main_Character.actorInterval("TorsoRunAnim", duration=4, loop=1)

    main_legsanim_wait = Main_Character.actorInterval("TorsoNeutralAnim", duration=2, loop=1)
    main_legsanim_run = Main_Character.actorInterval("LegsRunAnim", duration=4, loop=1)

    main_movement_wait = Main_Character.posInterval(2, Point3(1.2, 6.3, 0))
    main_movement_run = Main_Character.posInterval(4, Point3(-0.9, 9, 0))

    friend_torsoanim_rotate = Friend.actorInterval("TorsoWalkAnim", duration=2, loop=1)
    friend_torsoanim_run = Friend.actorInterval("TorsoRunAnim", duration=4, loop=1)

    friend_legsanim_rotate = Friend.actorInterval("LegsWalkAnim", duration=2, loop=1)
    friend_legsanim_run = Friend.actorInterval("LegsRunAnim", duration=4, loop=1)

    friend_movement_rotate = Friend.hprInterval(2, Vec3(30, 0, 0))
    friend_movement_run = Friend.posInterval(4, Point3(-1.5, 9, 0))

    main_torso_sequence = Sequence(main_torsoanim_wait, main_torsoanim_run)
    main_legs_sequence = Sequence(main_legsanim_wait, main_legsanim_run)
    main_movement_sequence = Sequence(main_movement_wait, main_movement_run)

    friend_torso_sequence = Sequence(friend_torsoanim_rotate, friend_torsoanim_run)
    friend_legs_sequence = Sequence(friend_legsanim_rotate, friend_legsanim_run)
    friend_movement_sequence = Sequence(friend_movement_rotate, friend_movement_run)

    main_torso_sequence.start()
    main_legs_sequence.start()
    main_movement_sequence.start()

    friend_torso_sequence.start()
    friend_legs_sequence.start()
    friend_movement_sequence.start()

    try:
        taskMgr.remove("camera18")
    except:
        pass
    
    def camera19(task):
        base.camera.setPos(0.5, 0, 3)
        base.camera.setHpr(0, -30, 0)
        return Task.cont
    taskMgr.add(camera19, "camera19")

def balcony_cleanup(): # Balcony Cleanup
    print "BC inst"
    global balcony_tiles
    try:
        for tile_list in balcony_tiles:
            for floor_tile in tile_list:
                floor_tile.removeNode()
        del balcony_tiles
    except NameError:
        print "BC BT NameError"

    global Lift_Cube
    try:
        Lift_Cube.removeNode()
        del Lift_Cube
    except NameError:
        print "BC LC NameError"

    global Art_Wall
    try:
        Art_Wall.removeNode()
        del Art_Wall
    except NameError:
        print "BC AW NameError"

    global ITL_Wall
    try:
        ITL_Wall.removeNode()
        del ITL_Wall
    except NameError:
        print "BC ITLW NameError"

    global SB_Wall
    try:
        SB_Wall.removeNode()
        del SB_Wall
    except NameError:
        print "BC SBW NameError"

    global ITL_Pillar
    try:
        ITL_Pillar.removeNode()
        del ITL_Pillar
    except NameError:
        print "BC ITLP NameError"

    global balcony_light1, balcony_light1_nodepath
    try:
        render.clearLight(balcony_light1_nodepath)
        balcony_light1_nodepath.removeNode()
        del balcony_light1, balcony_light1_nodepath
    except NameError:
        print "BC BL1 NameError"

    global balcony_light2, balcony_light2_nodepath
    try:
        render.clearLight(balcony_light2_nodepath)
        balcony_light2_nodepath.removeNode()
        del balcony_light2, balcony_light2_nodepath
    except NameError:
        print "BC BL2 NameError"

    global balcony_light3, balcony_light3_nodepath
    try:
        render.clearLight(balcony_light3_nodepath)
        balcony_light3_nodepath.removeNode()
        del balcony_light3, balcony_light3_nodepath
    except NameError:
        print "BC BL3 NameError"

    global balcony_fences
    try:
        for fence in balcony_fences:
            fence.removeNode()
        del balcony_fences
    except NameError:
        print "BC BF NameError"

    global grey_fog
    try:
        grey_fog.setExpDensity(0)
        render.clearFog()
        del grey_fog
    except NameError:
        print "BC GF NameError"

cur_scene = 1

def prev_scene():
    global cur_scene
    if cur_scene > 1:
        cur_scene -= 1
    eval("scene" + str(cur_scene) + "()")

def next_scene():
    global cur_scene
    if cur_scene < 19:
        cur_scene += 1
    eval("scene" + str(cur_scene) + "()")

base.accept("arrow_right", next_scene)
base.accept("arrow_left", prev_scene)

# Safe use of eval, I can assure you.
eval("scene" + str(cur_scene) + "()")



"""
# Music

Music = base.loader.loadSfx("phase_11/audio/bgm/LB_office.ogg")
Music.setLoop(True)
Music.setVolume(1.0)
Music.play()
"""



# base.oobe() lets you move around.
# Toggling this off gives you the camera view.

# base.run() runs the game loop.

#base.oobe()
base.run()
