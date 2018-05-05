"""
Copyright (C) 2018 kanishka-linux kanishka.linux@gmail.com

This file is part of vinanti.

vinanti is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

vinanti is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with vinanti.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import hashlib
import mimetypes

class Formdata:
    
    def __init__(self, form_dict, file_tuple):
        self.form_dict = form_dict
        self.file_tuple = file_tuple
        self.final_list = []
        boundary = '$@@#$#$#$#$#$#$#$#$#$#$#$#$#$@@$'
        boundary_bytes = bytes(boundary, 'utf-8')
        h = hashlib.sha256(boundary_bytes)
        self.boundary = h.hexdigest()
    
    def get_content_type(self, filename):
        return mimetypes.guess_type (filename)[0] or 'application/octet-stream'
    
    def arrange_files(self, value, boundary, new_boundary=None):
        file_type = self.get_content_type(value)
        file_name = os.path.basename(value)
        if new_boundary:
            self.final_list.append(bytes(new_boundary, 'utf-8'))
        else:
            self.final_list.append(bytes(boundary, 'utf-8'))
        if new_boundary:
            hdr = 'Content-Disposition: file; filename="{}"'.format('files', file_name)
        else:
            hdr = 'Content-Disposition: form-data; name="filedata"; filename="{}"'.format(file_name)
        self.final_list.append(bytes(hdr, 'utf-8'))
        hdr = 'Content-Type: {}'.format(file_type)
        self.final_list.append(bytes(hdr, 'utf-8'))
        self.final_list.append(b'')
        with open(value, 'rb') as f:
            content = f.read()
            self.final_list.append(content)
        
    def create_content(self):
        boundary = '--' + self.boundary
        for key, value in self.form_dict.items():
            self.final_list.append(bytes(boundary, 'utf-8'))
            hdr = 'Content-Disposition: form-data; name="{}"'.format(key)
            self.final_list.append(bytes(hdr, 'utf-8'))
            self.final_list.append(b'')
            self.final_list.append(bytes(value, 'utf-8'))
        if self.file_tuple and isinstance(self.file_tuple, str):
            self.arrange_files(self.file_tuple, boundary)
        else:
            for value in self.file_tuple:
                self.arrange_files(value, boundary)
        self.final_list.append(bytes(boundary+'--', 'utf-8'))
        self.final_list.append(b'')
        body = b'\r\n'.join (self.final_list)
        headers = {
            'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
            'Content-Length': str(len(body))
            }
        return body, headers
        
