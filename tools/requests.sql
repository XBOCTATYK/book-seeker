select cdp.*, cdpd.name from book_seeker.clean_data_param cdp join book_seeker.clean_data_params_dictionary cdpd ON cdpd.id = cdp."type" order by cdp.id desc
