from vkinder import app
from db.pipeline import make_pipeline

if __name__ == "__main__":
    main = app.APP.user_input()

    main.settings.load_settings(main.vk)
    main.check_settings()
    main.settings.add_settings()

    params = main.settings.make_flat_searc_params()
    base_params = main.settings.make_flat_searc_params(
        main.settings.get_base_searc())
    params.extend(base_params)

    if main.db.is_db_empty():
        users = main.progress_bar(
            params, main.vk.search, 'search in vk')
        main.progress_bar(users, main.db.save, 'normalize and save', one=True)

    pipeline = make_pipeline(main.settings.match)

    users = list(main.db.get(pipeline))

    if len(users) == 0:
        print('Никого не нашли. Попробуйте смягчить условия.')
    else:
        main.out(users)
        for user in users:
            main.db.set_skip(user['id'])
    main.settings.save_to_file()
