import requests
import re
import html2text
import os
import json


class Processor:
	def __init__(self, article_id, output_path, download_image=False, asset_path=None):
		self.article_id = article_id
		self.output_path = output_path
		self.download_image = download_image
		self.asset_path = asset_path
	
	def process(self):
		article_json = self._request_json()
  
		self.title = article_json['title']
		self.content = article_json['content']
		self.filename = os.path.join(self.output_path, self.title + '.md')
  
		self._process_content()
		self.markdown = html2text.html2text(self.content)

		self._process_markdown()


	def _request_json(self):
		
		article_api_url = f'https://api.zhihu.com/articles/{self.article_id}'
		config = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')))
    
		return requests.get(article_api_url, headers=config['headers'], cookies=config['cookies']).json()


	def _process_content(self):
     
		latex_pattern = r'<img src="https:\/\/www.zhihu.com\/equation\?tex=.*?" alt="(.*?)(\\tag\{\d+\})?" eeimg=".*?"\/>'
  
		def latex_repl(matchobj):
			tex = matchobj.group(1)
			tag = matchobj.group(2)
			if tag:
				return f'</p>$$zzdhyb{tex}byhdzz$$</p>'
			else:
				return f' $ {tex} $ '
		self.content = re.sub(latex_pattern, latex_repl, self.content)
  
		if not self.download_image:
			return

		image_pattern = r'<img src="(https?.+?)".+?/>'
  
		def image_repl(matchobj):
			image_url = matchobj.group(1)
			image_title = image_url.split('/')[-1]
			image_download_path = os.path.join(self.asset_path, image_title)
			image = requests.get(image_url).content
			with open(image_download_path, 'wb') as image_file:
				image_file.write(image)
			return f'<img src="{image_download_path}">'
		self.content = re.sub(image_pattern, image_repl, self.content)


	def _process_markdown(self):
   
		pattern = r'\\\\\\'
		self.markdown = re.sub(pattern, r'\\\\', self.markdown)
  
		pattern = r'\$\$\n*z\n*z\n*d\n*h\n*y\n*b(.*?)b\n*y\n*h\n*d\n*z\n*z\n*\$\$'
		def repl(matchobj):
			return f'$$\n{matchobj.group(1)}\n$$'
		self.markdown = re.sub(pattern, repl, self.markdown, flags=re.DOTALL)
  
		with open(self.filename, 'w') as output_file:
			output_file.write("# " + self.title + '\n\n')
			output_file.write(self.markdown)
