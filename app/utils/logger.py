class Logger:
    def log_info(info):
        ''' Print log information '''
        infoMessage = f'[INFO] {info}'
        print(infoMessage)

    def log_error(error):
        ''' send log errors cloudwatch '''
        errorMessage = f'[ERROR] {error}'
        print(errorMessage)

    def log_warning(warning):
        ''' send log errors cloudwatch '''
        warningMessage = f'[WARNING] {warning}'
        print(warningMessage)