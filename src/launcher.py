import Solution

def main():

    Solution.clean_up_files()
    Solution.unzip_files()
    Solution.dtcc_confirm_status()
    Solution.send_status_email()
    Solution.archive_files()


if __name__=='__main__':
    main()
