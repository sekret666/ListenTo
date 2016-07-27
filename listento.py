import telepot
from zaycevnet_parser import Parser

token = 'API_BOT_KEY'

parser = Parser()

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)
    query_string = query_string.replace(' ', '%20')
    url = 'http://go.mail.ru/zaycev?q=%s' % query_string
    page = parser.get_html_page(url)
    song_list = parser.get_song_list(page)
    print(song_list)
    bot.answerInlineQuery(query_id, song_list, cache_time=30)


bot = telepot.Bot(token)
bot.message_loop({
    'inline_query': on_inline_query
}, run_forever='Listening...')