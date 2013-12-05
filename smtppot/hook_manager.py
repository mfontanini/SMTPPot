import os, re, inspect, imp

class HookManager:
    # Match every .py file, except __init__.py
    file_filter_regex = re.compile('^(?!__init__).*\.py$')
    
    def __init__(self):
        self.__hooks = []
    
    def add_hook(self, hook):
        self.__hooks.append(hook)
    
    def run_hooks(self, mail):
        for hook in self.__hooks:
            hook.handle_email(mail)
        
    def load_hooks(self, hooks_dir):
        files = os.listdir(hooks_dir)
        files = filter(HookManager.file_filter_regex.search, files)
        for f in files:
            module = imp.load_source(f.split('.')[0], hooks_dir + "/" + f)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and 'handle_email' in dict(inspect.getmembers(obj)):
                    print '[+] Loading hook ' + name
                    self.add_hook(obj())
