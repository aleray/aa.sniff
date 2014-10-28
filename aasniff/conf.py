store = '/tmp/test'
sniffers = [
    'HttpSniffer',
    'HtmlSniffer',
    'RDFSniffer',
    'FeedSniffer',
    'ImageSniffer',
    'OggSniffer',
    'WavSniffer',
    'YoutubeSniffer'
]

#STORE = {
    #'ENGINE': 'sleepycat',
    #'NAME': '/tmp/foobaz',
#}

STORE = {
    'ENGINE': 'sqlite',
    'NAME': '/tmp/bar.db',
}

#STORE = {
    #'ENGINE': 'pgsql',
    #'NAME': 'mydatabase',
    #'USER': 'mydatabaseuser',
    #'PASSWORD': 'mypassword',
    #'HOST': 'localhost',
    #'PORT': '5432',
#}

#STORE = {
    #'ENGINE': 'mysql',
    #'NAME': 'foo',
    #'USER': 'foo',
    #'PASSWORD': 'bar',
    #'HOST': 'localhost',
    #'PORT': '5432',
#}
