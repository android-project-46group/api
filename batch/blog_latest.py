# TODO: autopep8 で整形したい
from typing import Literal
import json


class BlogLatest:
  # TODO: .ini で保持したい
  NOGI_BASE_URL: str = "https://blog.nogizaka46.com/"
  SAKURA_BASE_URL: str = "https://sakurazaka46.com/"
  HINATA_BASE_URL: str = "https://hinatazaka46.com/"

  def __init__( self, g_name ):
    self.g_name: Literal[ "nogizaka", "sakurazaka", "hinatazaka" ] = g_name
    self.save_path: Literal[ "imgs/nogi", "imgs/sakura", "imgs/hinata" ] = "imgs/" + g_name.replace( "zaka", "" )
    self.pic_base_url: Literal[
      "https://kokoichi0206.mydns.jp/imgs/blog/nogi",
      "https://kokoichi0206.mydns.jp/imgs/blog/sakura",
      "https://kokoichi0206.mydns.jp/imgs/blog/hinara"
    ] = "https://kokoichi0206.mydns.jp/imgs/blog/" + g_name.replace( "zaka", "" )
    self.base_url: str = (self.NOGI_BASE_URL if g_name == "nogizaka" else
      "{0}s/s46/diary/blog/list?ima=0000&ct=".format(self.SAKURA_BASE_URL) if g_name == "sakurazaka" else
      "{0}s/official/diary/member/list?ima=0000&ct=".format(self.HINATA_BASE_URL))

    self.headers = { "User-Agent": "Mozilla/5.0" }

  def get_scraping_images( self ):
    with open("./batch/settings.json") as f:
      infos: str = json.load(f)[ self.g_name ]
      
    for k, v in infos.items():
      print("{0}/{1}.jpg".format( self.pic_base_url, k ))
  
  def get_scraping_image( self, name: str, m_id: str ):
    pass


if __name__ == "__main__":
  # NOTE: CLI 実行であれば argparse 導入する
  t = BlogLatest( "sakurazaka" )
  t.get_scraping_images()