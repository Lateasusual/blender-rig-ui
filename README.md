# blender-rig-ui
Addon for Blender 2.80 for customisable rigging interfaces

Thanks for dropping by :)

# Installation
[Latest Release](https://github.com/Lateasusual/blender-rig-ui/releases)
Download as ZIP, then in Blender:
  Edit -> Preferences -> Add-ons -> Install... -> select blender-rig-ui.zip
  
# This is a lie, you'll need to rename it to RigUI_new for now, next update will need a reinstall since i'll rename the properties to work first time :)
  
# Usage
Still not quite as smooth as it ought to be...

  To create a UI:
  
 - Create a new collection for layout objects
 - Create a new text datablock to store layout in
 - VIEW_3D -> UI (N-panel) -> RigUI
 - Set Canvas Collection and Text Target to your collection and datablock
 - Add meshes to collection, set button colour and bone to link (0, 0 is the bottom left corner of the UI, so make sure everything is in positive X and Y, UI is from top down perspective (Numpad 7)
 - Build UI
 - Select Rig, set UI to the text block you built the UI into
 - You can delete the collection and the UI will remain, but obviously it will not be editable (hitting Build UI with an empty collection will give you an empty UI :) )
 
 To use the UI
 
 - Image editor -> Rig button on far left of header panel
 - Select the rig the UI is linked to :)
 (if you swap objects you might need to toggle pose mode for the UI to re-load)
 
# TODO
  - Zoom, currently UI is static size and offset from 0,0 in the bottom left
  - Literally every feature i want to add lol
  - Add canvas offset object, so UI layout doesn't have to be centred on origin while creating it
  - More as they come :)
