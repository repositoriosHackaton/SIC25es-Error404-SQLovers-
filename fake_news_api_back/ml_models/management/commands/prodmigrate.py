import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from termcolor import colored
from django.apps import apps
from datetime import datetime

class Command(BaseCommand):
    help = 'Custom command to run makemigrations and migrate for each app'
    
    def handle(self, *args, **kwargs):
        start_time = datetime.now()
        self.stdout.write(colored('\n╭────────────────────────────────────────────────────╮', 'cyan'))
        self.stdout.write(colored('│      STARTING AURA MIGRATE CUSTOM COMMAND          │', 'white', attrs=['bold']))
        self.stdout.write(colored('╰────────────────────────────────────────────────────╯\n', 'cyan'))
        
        #1 Makemigrations 
        self.stdout.write(colored('┌─ 📦 PHASE 1: MAKING MIGRATIONS', 'blue', attrs=['bold']))
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            self.stdout.write(colored(f'│  └─ 🔧 Processing: {app_label}...', 'blue'))
            try:
                call_command('makemigrations', app_label)
                self.stdout.write(colored(f'│     ✅ Migrations for {app_label} created successfully', 'green'))
            except Exception as e:
                self.stdout.write(colored(f'│     ❌ Error: {str(e)}', 'red'))
        
        #2 Migrate all makemigrations builded
        self.stdout.write(colored('│\n├─ 🚀 PHASE 2: APPLYING MIGRATIONS', 'blue', attrs=['bold']))
        try:
            call_command('migrate')
            self.stdout.write(colored('│  └─ ✅ All migrations applied successfully', 'green'))
        except Exception as e:
            self.stdout.write(colored(f'│  └─ ❌ Error: {str(e)}', 'red'))
            
        #3 Final message
        self.stdout.write(colored('│\n└─  COMPLETED', 'blue', attrs=['bold']))
        self.stdout.write(colored('\n╭────────────────────────────────────────────────────╮', 'cyan'))
        self.stdout.write(colored(f'│   Database: {settings.DATABASES["default"]["NAME"]} ', 'white'))
        elapsed_time = datetime.now() - start_time
        self.stdout.write(colored(f'│   Time elapsed: {elapsed_time}', 'white'))
        self.stdout.write(colored('╰────────────────────────────────────────────────────╯\n', 'cyan'))