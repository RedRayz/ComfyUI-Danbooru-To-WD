# ComfyUI-Danbooru-To-WD
 Converts booru tags to a format suitable for Waifu Diffusion(or Danbooru based models).
 
 BooruタグをWaifu Diffusion(あるいはDanbooruベースのモデル)のフォーマットに変換するAUTOMATIC1111 Stable diffusion WebUIの拡張機能です。
 
 Example: `1girl blonde_hair blue_eyes name_(copyright) upper_body` -> `1girl, blonde hair, blue eyes, name \(copyright\), upper body`
 
 booru_tagsにタグを入力する以外に、booru_urlに一部Booruサイトの投稿URLを入力しても変換できます。URLからであればAnimagine推奨の並びにできます。
 
 WebUIのExtensionからの単なる移植であり大した機能はありません。ご了承ください。

## 注意
 Animagine推奨の並びにできるのはURLからのみとなります。

 booru_urlが指定されている場合はそちらが優先されます。

 booru_urlに指定されたURLが間違っているかサイトがjson以外を返すとエラーになります。
