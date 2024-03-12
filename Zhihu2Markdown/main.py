from processor import Processor
import argparse
import re
import os

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Transform zhihu article to Markdown format')
	parser.add_argument('article_url', help='URL of zhihu article')
	parser.add_argument('-i', '--image_dir', help='If present, download image to the image dir path')

	args = parser.parse_args()
 
	output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DownloadMarkdown')
 
	if args.image_dir:
		download_image = True
		asset_path = args.image_dir
	else:
		download_image = False
		asset_path = None

	article_url = args.article_url
	article_pattern = r'https://zhuanlan.zhihu.com/p/(\d.+)/?'
	objmatch = re.search(article_pattern, article_url)
	article_id = objmatch.group(1)
 
	if not article_id:
		raise "Article URL not match. Must like: https://zhuanlan.zhihu.com/p/1234567"

	article = Processor(article_id, output_path, download_image, asset_path)
	article.process()
