# Astrology - web

![](../images/b9d648e3-5f31-4ba9-ba37-bc3c34c27b76.png)

Po odpaleniu lokalnego serwera z `from astroquery import log; log.setLevel("DEBUG")` okazuje się, że przy pobieraniu plików funkcją `ALMA().download_files`, Astroquery cacheuje klasę `Request` pickleując ją:

![](../images/d314be33-d11b-47cd-8f91-5dedf8f28560.png)

Używając `dataarchive_url` możemy zqueryować nasze podstawione API, który odpowie, żeby pobrać malicious pickle'a do miejsca wskazanego przez `Content-Disposition` header (path traversal). Nazwa zcacheowanego response'a to tak naprawdę hash klasy `AstroQuery`.

Przy drugim query, AstroQuery spróbuje zdeserializować zcacheowany request, gdzie przez insecure deserialization możemy skopiować flagę do `/static/downloads/xxxx.txt` i stamtąd ją pobrać. 

![](../images/c47b662a-beda-4fbf-ad99-7e31a7a5bde8.png)

Flag: `ecsc23{0day_RCE_if_astronomer_downloads_a_file_from_you}`
