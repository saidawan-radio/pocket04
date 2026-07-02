from FetchDetail import load_json,dump_json, load_datetime
from config import conf

origin_data = load_json(conf.ORIGIN_DATA_FILE_PATH)
downloaded_data = load_json(conf.DOWNLOADED_DATA_FILE_PATH)
for dldetail in downloaded_data["audio_info"].values():
    internal_id = dldetail["id"]
    if internal_id in origin_data["audio_info"]:
        orgdetail = origin_data["audio_info"][internal_id]
        if load_datetime(dldetail["edit_date"], conf.DATE_FORMAT) < load_datetime(orgdetail["edit_date"],conf.DATE_FORMAT):
            print("Update:", orgdetail["id"], orgdetail["msg_id"], orgdetail["title"])
            dldetail["title"] = orgdetail["title"]
            dldetail["performer"] = orgdetail["performer"]
            dldetail["message"] = orgdetail["message"]
            dldetail["edit_date"] = orgdetail["edit_date"]
    

dump_json(conf.DOWNLOADED_DATA_FILE_PATH, downloaded_data)
        