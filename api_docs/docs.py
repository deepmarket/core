API = {
    "base": "https://api.deepmarket.cs.pdx.edu/api/v1",
    "__base": "http://atlantic.cs.pdx.edu:8080/api/v1",
    "user": {
        "firstname": "Barabara", 
        "lastname": "Streisand", 
        "email": "barbara@email.com", 
        "password": "password"
    },
    "endpoints": [
        {
            "name": "account",
            "endpoint": "/account",
            "desc": "Get account information",
            "methods": [
                # endpoint, params, requires token
                ["GET", "/account/", "{}", True],
                ["POST", "/account/", "{firstname, lastname, email, password}", False],
                ["PUT", "/account/", "{}", True],
                ["DELETE", "/account/", "{}", True]
            ]
        },
        {
			"name": "authentication",
            "endpoint": "/auth",
            "desc": "Login to the application (i.e. generate an auth token)",
            "methods": [
                ["POST", "/auth/login", "{email, password}", False],
                ["POST", "/auth/logout", "{}", True],
            ]
        },
        {
            "name": "resources",
            "endpoint": "/resources",
            "desc": "Get resource information",
            "headers": ["method", "endpoint", "parameters", "requires token", "notes"],
            "modifiers": ["as_raw", "as_code", "as_code", "as_raw", "as_raw"],
            "methods": [
                ["GET", "/resources/", "{}", True, ""],
                ["POST", "/resources/", "{ip_address, ram, cores, cpus, gpus, price, machine_name}", True, ""],
                ["PUT", "/resources/{resource_id}", "{}", True, ""],
                ["DELETE", "/resources/", "{}", True, "**deprecated**: Use `/{resource_id}` instead."],
                ["DELETE", "/resources/{resource_id}", "{}", True, ""]
            ]
        },
        {
			"name": "jobs",
            "endpoint": "/jobs",
            "desc": "Get job information",
            "headers": ["method", "endpoint", "parameters", "requires token", "notes"],
            "modifiers": ["as_raw", "as_code", "as_code", "as_raw", "as_raw"],
            "methods": [
                ["GET", "/jobs/", "{}", True, ""],
                ["GET", "/jobs/{job_id}", "{}", True, ""],
                ["POST", "/jobs/", "{workers, cores, memory, timeslot_id, price, source_files, input_files}", True, ""],
                ["PUT", "/jobs/{job_id}", "{}", True, "*NOT IMPLEMENTED*"],
                ["DELETE", "/jobs/{job_id}", "{}", True, ""]
            ]
        },
        {
			"name": "pricing",
            "endpoint": "/pricing",
            "desc": "Get pricing information",
            "methods": [
                ["GET", "/pricing/", "{}", False],
                ["POST", "/pricing/", "TBD", True]
            ]
        }
    ]
}

class Docs(object):
    def __init__(self, *args, **kwargs):
        self.md = MD("")
        self.base = API["__base"]
        self.curl = Curl(self.base)
        self.curl.call(request="POST", endpoint="/auth/login/", data=API["user"])

        # self.gen_api_overview()

        self.output = self.md.get()
        print(self.output)

    def gen_api_overview(self, uses: list=["curl"]):
        
        modifiers = [self.md.as_raw, self.md.as_code, self.md.as_code, self.md.as_raw]

        for endpoint in API["endpoints"]:
            name = endpoint["name"]
            
            headers = endpoint.get("headers", ["method", "endpoint", "parameters", "requires token"])
            modifiers = endpoint.get("modifiers", [self.md.as_raw, self.md.as_code, self.md.as_code, self.md.as_raw])
            
            # Get mod functions from string of function name if using custom mods
            if len(modifiers) is not 4:
                modifiers = [getattr(self.md, mod) for mod in modifiers]

            # Map modifiers to body cells
            body = [
                [f(item) for f, item in zip(modifiers, row)] for row in endpoint.get("methods")
            ]

            self.md.heading(f"{name.capitalize()} ({endpoint.get('endpoint')})", 3) \
                .p(f"An overview of the {endpoint['name']} endpoint:") \
                .table(headers, body) \
                .hr() \
                .get()

            for row in endpoint.get("methods"):
                method = row[0]

                self.md.heading("Request", 6) \
                    .p("\n\n") \
                    .code(f"{method} {self.base}") \
                    .p("\n\nUsing ") \
                    .code("curl")

                request = self.gen_request()
                
    
    def gen_request(self,):
        pass

    def gen_response(self,):
        pass

        return self

class Output(object):
    def __init__(self, *args, **kwargs):
        pass

    def as_raw(self, text: str="", endl=""):
        return rf"{text}{endl}"
    
    def as_code(self, text: str or [], lang: str=None):
        if lang is not None:
            return self.as_raw(f"```{lang}\n{text}\n```")
        else:
            return self.as_raw(f"`{text}`")

class MD(Output):
    def __init__(self, base_str: str="", *args, **kwargs):
        self.base_str = base_str
    
    def get(self):
        return self.base_str

    def hr(self):
        self.base_str += self.as_raw("\n***\n")
        return self
    
    def heading(self, text: str="", size: int=1):
        if size > 6:
            size = 6

        self.base_str += self.as_raw(f"\n{'#' * size} {text}\n")
        return self
    
    def link(self, text: str="", link: str=""):
        self.base_str += self.as_raw(f"[{text}]({link})")
        return self

    def code(self, text: str or [], lang: str=None):
        if lang is not None:
            self.base_str += self.as_raw(f"```{lang}\n{text}\n```")
        else:
            self.base_str += self.as_raw(f"`{text}`")
        return self
    
    def p(self, text: str=""):
        self.base_str += self.as_raw(f"\n\n{text}\n\n")
        return self
    
    def _add_header(self, headers, column_widths):
        header_text: str = "|"
        for i, header in enumerate(headers):
            max_col_width = max(column_widths[i])
            padding = (max_col_width - len(header))
            header_text += self.as_raw(f" {header}" + " " * padding + " |")
        
        header_text += self.as_raw("\n" "|")
        for col in column_widths:
            max_col_width = max(col)
            # Add 2 to `max_col_width` for spaces on either side of header text
            header_text += self.as_raw("-" * (max_col_width + 2) + "|")

        return header_text

    def _add_body(self, body, column_widths):
        body_text = ""
        for row in body:
            body_text += "|"
            for i, col_body in enumerate(row):
                max_col_width = max(column_widths[i])
                padding = (max_col_width - len(str(col_body)))
                body_text += self.as_raw(f" {col_body}" + " " * padding + " |")

            body_text += self.as_raw("\n")

        return body_text

    def table(self, headers: [], body: [[]]):
        header_len = len(headers)

        # Check for valid table size
        for i, row in enumerate(body):
            if len(row) > header_len:
                raise ValueError(f"Row {i + 1} of body has too many columns.\n\t{row}")

        column_widths = []

        # Get widths of the columns in the table where each subarray 
        # is column and each index of subarray is row
        for i, header in enumerate(headers):
            column_widths.append([len(str(header))])
            for row in body:
                column_widths[i].append(len(str(row[i])))

        table_text = self._add_header(headers, column_widths)
        table_text += self.as_raw("\n")
        table_text += self._add_body(body, column_widths)

        self.base_str += table_text
        return self

    def print(self, text: str=""):
        print(self.as_raw(text))
    
class Call(object):
    def __init__(self, *args, **kwargs):
        pass
    
class Curl(Call):
    
    def __init__(self, base_url: str="", *args, **kwargs):
        self.base_url = base_url
        self.token: str = None

        self.template = """curl --request {request} --header '{header}' --data '{data}' {base_url}{endpoint}"""
    
    def call(self, request: str="GET", endpoint: str="", header: str="Content-Type: application/json", data: str=""):
        from json import dumps
        from os import system
        from subprocess import call

        json_data = dumps(data)
        call_string = self.template.format(request=request, header=header, data=json_data, base_url=self.base_url, endpoint=endpoint)
        
        print(call_string)
        print(call(call_string))
        # if status is not 0:
        #     print(f"NOTICE: {call_string[:10]}...{call_string[-10:]} returned {status}")
        
        # return ret
        



if __name__ == "__main__":
    docs = Docs()
    