"""Regenerate blog discovery metadata after editing posts. Requires beautifulsoup4."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html, json, re, subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / 'blogger-migration.json').exists():
 raise SystemExit('This site has migrated to Blogger. Do not regenerate the legacy blog metadata; see README.md.')
ORIGIN = 'https://seominseok0429.github.io'
POST = '/blog/posts/when-ai-believes-a-false-reality/'
IMAGE = ORIGIN + POST + 'images/trex-transformed.png'
DESCRIPTIONS = {
 'ko': '서민석의 AI 안전성 실험: 시각적으로 변환된 장면이 OpenAI Astra와 Anthropic Fable의 판단에 미치는 영향. 원본·변환 이미지, 시뮬레이터 예시와 한계를 공유합니다.',
 'en': 'Minseok Seo explores how altered visual scenes affect OpenAI Astra and Anthropic Fable, with image comparisons, simulator examples, and discussion of AI safety risks and limitations.',
 'zh-CN': 'Minseok Seo 的 AI 安全实验：视觉转换如何影响 OpenAI Astra 与 Anthropic Fable 的判断。包含原图对比、模拟器示例及风险与局限讨论。'
}
COLLECTIONS = {
 '/blog/': 'Minseok Seo’s research notebook: AI safety experiments, research papers, and things tried, shared openly in Korean, English, and Chinese.',
 '/blog/open-experiments/': 'Things I tried: Minseok Seo’s open experiments and notes, including visual perception and AI safety.',
 '/blog/my-papers/': 'Research paper notes by Minseok Seo. Papers, because I need a job.'
}
records=[]
for p in sorted((ROOT/'blog').rglob('index.html')):
 source=p.read_text(); soup=BeautifulSoup(source,'html.parser')
 canonical=soup.find('link',rel='canonical')
 url=ORIGIN+'/'+p.relative_to(ROOT).parent.as_posix()+'/'
 if not canonical or canonical.get('href')!=url: continue  # Skip legacy redirects.
 lang=soup.html.get('lang','en'); is_post=bool(soup.select_one('.post-body'))
 desc=DESCRIPTIONS[lang] if is_post else COLLECTIONS[url.removeprefix(ORIGIN)]
 title=soup.title.get_text(); headline=soup.h1.get_text(' ',strip=True)
 # Only replace the metadata block; retain the visible page exactly.
 source=re.sub(r'<meta\b(?=[^>]*name="description")[^>]*>', '<meta name="description" content="'+html.escape(desc,quote=True)+'">',source)
 def meta(k,v,property=False): return '<meta '+('property' if property else 'name')+'="'+k+'" content="'+html.escape(v,quote=True)+'">'
 tags=[meta('robots','index, follow, max-image-preview:large'),meta('author','Minseok Seo')]
 for k,v in {'og:type':'article' if is_post else 'website','og:site_name':'Minseok Seo · Notes on research','og:title':title,'og:description':desc,'og:url':url,'og:image':IMAGE,'og:image:width':'1672','og:image:height':'941','og:image:alt':'Original scene transformed into Tyrannosauruses for an AI safety experiment','og:locale':{'ko':'ko_KR','en':'en_US','zh-CN':'zh_CN'}[lang]}.items(): tags.append(meta(k,v,True))
 tags += [meta('twitter:card','summary_large_image'),meta('twitter:title',title),meta('twitter:description',desc),meta('twitter:image',IMAGE),'<link rel="alternate" type="application/rss+xml" title="Minseok Seo · Blog" href="'+ORIGIN+'/blog/feed.xml">']
 person={'@type':'Person','@id':ORIGIN+'/#person','name':'Minseok Seo','url':ORIGIN+'/'}
 schema={'@context':'https://schema.org','@type':'BlogPosting' if is_post else 'CollectionPage','@id':url+'#'+('article' if is_post else 'page'),'url':url,'name':headline,'description':desc,'inLanguage':lang,'author':person,'isPartOf':{'@type':'Blog','@id':ORIGIN+'/blog/#blog','name':'Notes on research','url':ORIGIN+'/blog/'}}
 modified=subprocess.check_output(['git','log','-1','--format=%cs','--',str(p.relative_to(ROOT))],cwd=ROOT,text=True).strip()
 if is_post:
  published=soup.select_one('.post-meta time')['datetime']
  schema.update(headline=headline,image=[IMAGE],datePublished=published,dateModified=modified,mainEntityOfPage={'@type':'WebPage','@id':url},articleSection='Things I tried')
  tags += [meta('article:published_time',published,True),meta('article:modified_time',modified,True),meta('article:author',ORIGIN+'/',True)]
  for alt in soup.select('link[hreflang]'):
   if alt['hreflang'] not in (lang,'x-default'): tags.append(meta('og:locale:alternate',{'ko':'ko_KR','en':'en_US','zh-CN':'zh_CN'}[alt['hreflang']],True))
 tags.append('<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>')
 block='<!-- SEO:START -->\n'+'\n'.join(tags)+'\n<!-- SEO:END -->'
 if re.search(r'<!-- SEO:START -->.*?<!-- SEO:END -->',source,flags=re.S):
  source=re.sub(r'<!-- SEO:START -->.*?<!-- SEO:END -->',lambda _: block,source,count=1,flags=re.S)
 else:
  source=source.replace('</head>','\n'+block+'\n</head>')
 p.write_text(source)
 records.append((url,modified,soup,is_post,desc))

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
sitemap=ET.Element(ns+'urlset')
ET.SubElement(ET.SubElement(sitemap,ns+'url'),ns+'loc').text=ORIGIN+'/'
for url,modified,soup,is_post,desc in records:
 entry=ET.SubElement(sitemap,ns+'url');ET.SubElement(entry,ns+'loc').text=url
 if modified: ET.SubElement(entry,ns+'lastmod').text=modified
 if is_post:
  for link in soup.select('link[hreflang]'): ET.SubElement(entry,'{http://www.w3.org/1999/xhtml}link',rel='alternate',hreflang=link['hreflang'],href=link['href'])
ET.indent(sitemap)
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
# Plain-text fallback for search engines; keep the URL list identical.
(ROOT/'sitemap.txt').write_text('\n'.join(el.text for el in sitemap.iter(ns+'loc'))+'\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
ET.register_namespace('atom','http://www.w3.org/2005/Atom')
rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
for key,value in [('title','Minseok Seo · Notes on research'),('link',ORIGIN+'/blog/'),('description',COLLECTIONS['/blog/']),('language','ko')]: ET.SubElement(channel,key).text=value
ET.SubElement(channel,'{http://www.w3.org/2005/Atom}link',href=ORIGIN+'/blog/feed.xml',rel='self',type='application/rss+xml')
for url,modified,soup,is_post,desc in records:
 if not is_post or soup.html['lang']!='ko': continue
 item=ET.SubElement(channel,'item')
 for key,value in [('title',soup.h1.get_text(' ',strip=True)),('link',url),('description',desc),('category','Things I tried')]:ET.SubElement(item,key).text=value
 ET.SubElement(item,'guid',isPermaLink='true').text=url
ET.indent(rss);ET.ElementTree(rss).write(ROOT/'blog/feed.xml',encoding='utf-8',xml_declaration=True)
print('Generated metadata for',len(records),'pages, sitemap and RSS.')
