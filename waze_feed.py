import os
import json
import sys
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def process_end_time():
   *tz = ZoneInfo("Australia/Hobart")
*   now = datetime.now(tz)

    # K*ep a reported closure active for 2* hours.
    # The GitHub workflow *ill refresh this every five minute*.
    end_time = now + timedelta(h*urs=24)

    return end_time.strft*me('%Y-%m-%dT%H:%M:%S%z')
    
    def main():
	    print("--- I*itiating City of Hobart Road Statu* Feed Generator ---")

	    payload*file = "road_status.json"

    if *ot os.path.exists(payload_file):
 *      print("CRITICAL ERROR: No Cl*udflare Worker data file detected.*)
        sys.exit(1)

    try:
  *     with open(payload_file, "r", *ncoding="utf-8") as f:
           *payload = json.load(f)

    except*(json.JSONDecodeError, FileNotFoun*Error) as e:
        print(f"CRITI*AL ERROR: Invalid Worker JSON file* {e}")
        sys.exit(1)

    ga*e_status = str(payload.get("status*, "")).strip()
    updated = str(p*yload.get("updated", "")).strip()
*   closed_gate = payload.get("clos*dGate")
    gates = payload.get("g*tes", [])

    if not gate_status:*        print("CRITICAL ERROR: The*Cloudflare Worker returned a blank*status.")
        sys.exit(1)

   *print(f"[Worker] Road status: {gat*_status}")
    print(f"[Worker] La*t updated: {updated or 'Not suppli*d'}")
    print(f"[Worker] Closed *ate value: {closed_gate}")
    pri*t(f"[Worker] Gate records received* {len(gates)}")

    
    # polyline coordinate pairs
    geometries = {
        "bracken_lane_to_the_springs": "-42.91670631 147.2610976360632 -42.91598368 147.25996401661425 -42.91481034 147.25921644182654 -42.91413309 147.25794978066708 -42.91354169 147.25809349599612 -42.91238499 147.25735070264878 -42.9119826 147.25595937688965 -42.91270738 147.25111480333513 -42.91203479 147.25006559022316 -42.91164707 147.24846748779942 -42.91126128 147.2483857 -42.90919358 147.24816448175682 -42.90843337 147.24802253550783 -42.9085152 147.24777779919341 -42.90909083 147.24771848458067 -42.91019066 147.24710223090986 -42.91116439 147.24684811523696 -42.91321151 147.24763164043802 -42.91373003 147.24907553589424 -42.91456439 147.25069924727535 -42.91471278 147.2521457321526 -42.91493078 147.25229856445165 -42.91659614 147.25098622235652 -42.91721892 147.2507746671974 -42.91471526 147.2476687771719 -42.91434162 147.24646988410942 -42.91362693 147.24579112779264",
        "the_springs_to_the_pinnacle": "-42.91351415 147.24569046382496 -42.91336039 147.24560034599207 -42.91118213 147.24407386871715 -42.90526122 147.2443283892155 -42.90321386 147.24305438140115 -42.89965989 147.24384449365613 -42.89459553 147.24465672316097 -42.89053484 147.24210076203087 -42.88968326 147.23525678232053 -42.88930066 147.23391407220672 -42.88785692 147.22804135377962 -42.88609205 147.22218977029482 -42.88510764 147.22203911301335 -42.88508269 147.22162148118855 -42.88590796 147.2208250860001 -42.8897646 147.22100454729207 -42.89003245 147.22118648270654 -42.89109175 147.22398620511052 -42.89245291 147.22572027497998 -42.89151891 147.22716958279926 -42.89150723 147.2297719017168 -42.89551625 147.23772122500006",
        "springs_one_way": "-42.91530699 147.24828411497148 -42.91471526 147.2476687771719 -42.91434162 147.24646988410942 -42.91362693 147.24579112779264"
        }
    
       status_l*wer = gate_status.lower()

    # E*pected Worker statuses include:
  * # "Road open to Pinnacle"
    # "*oad closed at The Springs"
    # "*oad closed at Bracken Lane"

    i* (
        "open to pinnacle" in s*atus_lower
        or "open to the*pinnacle" in status_lower
        *r "open to summit" in status_lower*        or "open to the summit" in*status_lower
    ):
        is_clo*ed_at_bracken = False
        is_c*osed_at_springs = False

    elif *bracken" in status_lower:
        * A closure at Bracken Lane closes *oth mapped sections.
        is_cl*sed_at_bracken = True
        is_c*osed_at_springs = True

    elif "*pring" in status_lower:
        # * closure at The Springs only close* the upper section.
        is_clo*ed_at_bracken = False
        is_c*osed_at_springs = True

    else:
*       print(
            f"CRITIC*L ERROR: Unrecognised road status:*{gate_status}"
        )
        p*int(
            "The existing pub*ic feed will be retained rather th*n "
            "publishing an inc*rrect status."
        )
        s*s.exit(1)

    is_springs_one_way * False
    
        # Establish local execution ti*e using the Hobart timezone.
    n*w_local = datetime.now(ZoneInfo("A*stralia/Hobart"))
    starttime_is* = now_local.strftime("%Y-%m-%dT%H*%M:%S%z")
    endtime_iso = proces*_end_time()

    description_time * updated or "update time not supplied"
    
    waze_data = {"incidents": []}
    
    # Segment A: Bracken Lane to The Springs
    if is_closed_at_bracken:
        # Generate unique ID 
        incident_id = str(uuid.uuid4())
    
        waze_data["incidents"].append({
            "incident": {
                "id": incident_id,
                "type": "ROAD_CLOSED",
                "subtype": "ROAD_CLOSED_HAZARD",
                "polyline": geometries["bracken_lane_to_the_springs"],
                "street": "Pinnacle Road",
                "starttime": starttime_iso,
                "endtime": endtime_iso,
                "description": f"City of Hobart road status: {gate_status}. Last updated: {description_time}.",
                "direction": "BOTH_DIRECTIONS"
            }
        })
        print("Success: Validated incident object generated for pinnacle_rd_closed_bracken.")
        
    # Segment B: The Springs to the Pinnacle
    if is_closed_at_springs:

        # Generate unique ID 
        incident_id = str(uuid.uuid4())
    
        waze_data["incidents"].append({
            "incident": {
                "id": incident_id,
                "type": "ROAD_CLOSED",
                "subtype": "ROAD_CLOSED_HAZARD",
                "polyline": geometries["the_springs_to_the_pinnacle"],
                "street": "Pinnacle Road",
                "starttime": starttime_iso,
                "endtime": endtime_iso,
                "description": f"City of Hobart road status: {gate_status}. Last updated: {description_time}.",
                "direction": "BOTH_DIRECTIONS"
            }
        })
        print("Success: Validated incident object generated for pinnacle_rd_closed_springs.")

        # Segment C: The Springs - one way road closure
        
        if is_springs_one_way:
            # Generate unique ID 
            incident_id = str(uuid.uuid4())
    
            waze_data["incidents"].append({
                "incident": {
                "id": incident_id,
                "type": "ROAD_CLOSED",
                "subtype": "ROAD_CLOSED_HAZARD",
                "polyline": geometries["springs_one_way"],
                "street": "Pinnacle Road",
                "starttime": starttime_iso,
                "endtime": endtime_iso,
                "description": f"City of Hobart road status: {gate_status}. Last updated: {description_time}.",
                "direction": "ONE_DIRECTION"
            }
        })
        print("Success: Validated incident object generated for pinnacle_rd_one_way_springs.")
        
    if not waze_data["incidents"]:
        print("Evaluation complete: Road is OPEN. Generating empty incidents list.")
        
    os.makedirs("dist", exist_ok=True)
    try:
        with open("dist/waze_closure_feed.json", "w") as f:
            json.dump(waze_data, f, indent=2)
        print("Waze JSON closure feed generated inside dist/ folder successfully.")
    except IOError as e:
        print(f"CRITICAL ERROR: Failed to write Waze feed file to disk: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
