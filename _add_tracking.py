"""Add Newsbreak Pixel + Microsoft Clarity to all funnel pages."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
NEWSBREAK_PIXEL_ID = "ID-2032552853944918018"
CLARITY_ID = "whxdotwqls"

def make_head_snippet(funnel_step):
    return (
        '<!-- Newsbreak Pixel -->\n'
        '<script>\n'
        "!(function(e,n,t,i,p,a,s){e[i]||(((p=e[i]=function(){p.process?p.process.apply(p,arguments):p.queue.push(arguments)}).queue=[]),(pt=+new Date),((a=n.createElement(t)).async=1),(a.src='https://static.newsbreak.com/business/tracking/nbpixel.js?t='+864e5*Math.ceil(new Date/864e5)),(s=n.getElementsByTagName(t)[0]).parentNode.insertBefore(a,s))})(window,document,'script','nbpix'),\n"
        f"nbpix('init','{NEWSBREAK_PIXEL_ID}'),\n"
        "nbpix('event','page_view'),\n"
        f"nbpix('event','{funnel_step}');\n"
        '</script>\n'
        '<!-- /Newsbreak Pixel -->\n'
        '<!-- Microsoft Clarity -->\n'
        '<script type="text/javascript">\n'
        '(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})'
        f'(window,document,"clarity","script","{CLARITY_ID}");\n'
        f'clarity("event","{funnel_step}");\n'
        f'clarity("set","funnel_step","{funnel_step}");\n'
        '</script>\n'
        '<!-- /Microsoft Clarity -->\n'
        '</head>'
    )

PAGES = {
    'index.html':     'advertorial_view',
    'quiz.html':      'quiz_started',
    'result.html':    'quiz_completed',
    'resultado.html': 'quiz_completed_pt',
    'checkout.html':  'viewed_offer',
    'thankyou.html':  'purchase_complete',
}

for fname, step in PAGES.items():
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        print(f'  X {fname}: not found')
        continue
    content = open(fpath).read()
    if 'nbpixel' in content or 'clarity.ms/tag' in content:
        print(f'  o {fname}: tracking already there, skip')
        continue
    snippet = make_head_snippet(step)
    new_content = content.replace('</head>', snippet, 1)
    if new_content == content:
        print(f'  X {fname}: </head> not found')
        continue
    open(fpath, 'w').write(new_content)
    print(f'  + {fname}: tracking added (funnel_step={step})')

# Add Stripe button click tracking on checkout.html
print()
print('Adding Stripe button click tracking to checkout.html...')
fpath = os.path.join(BASE, 'checkout.html')
content = open(fpath).read()

stripe_handler = (
    '<script>\n'
    '/* Tracking: fire initiate_checkout on Stripe button clicks */\n'
    '(function(){\n'
    "  var packPrices = {'2': 99, '3': 129, '6': 199};\n"
    "  document.addEventListener('DOMContentLoaded', function(){\n"
    '    document.querySelectorAll(\'a[href*="buy.stripe.com"]\').forEach(function(btn){\n'
    "      btn.addEventListener('click', function(){\n"
    "        var pack = btn.getAttribute('data-pack') || '3';\n"
    '        var value = packPrices[pack] || 129;\n'
    "        if(typeof nbpix === 'function'){\n"
    "          try { nbpix('event','initiate_checkout',{ nb_value: value }); } catch(e) {}\n"
    '        }\n'
    "        if(typeof clarity === 'function'){\n"
    '          try {\n'
    "            clarity('event','initiate_checkout');\n"
    "            clarity('set','plan_clicked', pack + '-jar');\n"
    "            clarity('set','order_value', String(value));\n"
    '          } catch(e) {}\n'
    '        }\n'
    '      });\n'
    '    });\n'
    '  });\n'
    '})();\n'
    '</script>\n'
    '</body>'
)

if 'initiate_checkout' not in content:
    new_content = content.replace('</body>', stripe_handler, 1)
    if new_content != content:
        open(fpath, 'w').write(new_content)
        print('  + checkout.html: Stripe click tracking added')
    else:
        print('  X checkout.html: </body> not found')
else:
    print('  o checkout.html: initiate_checkout handlers already exist')

print('\nDONE.')
