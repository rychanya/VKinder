from vkinder import app
from db.pipeline import make_pipeline

if __name__ == "__main__":
    main = app.APP.user_input()
    main.load_settings()
    main.check_settings()
    if main.db.is_db_empty():
        users = main.progress_bar(
            main.make_flat_searc_params(), main.vk.search, 'search in vk')
        main.progress_bar(users, main.db.save, 'normalize and save', one=True)

    pipeline = make_pipeline(main.match_params, main.intersection_params)

    users = list(main.db.get(pipeline))
    if len(users) == 0:
        print('Никого не нашли. Попробуйте смягчить условия.')
    else:
        main.out(users)
        for user in users:
            main.db.set_skip(user['id'])
    main.save_settings_to_db()
    main.save_settings_to_file()
