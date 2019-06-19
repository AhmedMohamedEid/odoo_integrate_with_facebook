# -*- coding: utf-8 -*-

from odoo import models, fields, api
import facebook
from datetime import datetime



class FacebookPagesConfig(models.Model):
    _name = 'facebook.pages.config'
    _rec_name = 'name'
    _description = 'Facebook Pages'

    name = fields.Char(string="Page Name", required=True, )
    access_token = fields.Char(string="Access Token", required=True, )
    page_id = fields.Char(string="Page ID", required=True, )
    fb_api_version = fields.Char(string="Graph API", default="3.3", required=False, )





class FacebookPosts(models.Model):
    _name = 'facebook.posts'
    _rec_name = "title"
    _description = 'Posts for publish to facebook'

    title = fields.Char(string="Title", required=False, )
    page_config_id = fields.Many2one(comodel_name="facebook.pages.config", string="Pages", required=True, )
    publish_date = fields.Datetime(string="Published On" )

    message = fields.Text(string="Messege", required=True, )

    on_create_date = fields.Datetime(string="Create On", default=fields.Datetime.now(), required=False, )

    facebook_post_id = fields.Char(string="Facebook ID", required=False, )

    link = fields.Char(string="Link", required=False, )

    image = fields.Binary(string="Image")

    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('publish', 'Published'), ], default="draft" ,required=False, )

    comments_ids = fields.One2many(comodel_name="fb.post.comment", inverse_name="post_id", string="Comments", required=False, )


    # def access_token(self):
    #     graph = facebook.GraphAPI(access_token=self.page_config_id.access_token,
    #                               version=self.page_config_id.fb_api_version)
    #     return graph



    import tempfile
    import base64
    import os

    from PIL import Image

    from openerp import models, fields, api
    from openerp.exceptions import UserError

    class MyModel(models.Model):
        [...]
        image = fields.Binary()

        @api.multi
        def open_image(self):
            self.ensure_one()
            if not self.image:
                raise UserError("no image on this record")
            # decode the base64 encoded data
            data = base64.decodestring(self.image)
            # create a temporary file, and save the image
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            # open the image with PIL
            try:
                image = Image.open(fname)
                # do stuff here
            finally:
                # delete the file when done
                os.unlink(fname)

    def publish_post_facebook(self):

        graph = facebook.GraphAPI(access_token=self.page_config_id.access_token, version=self.page_config_id.fb_api_version)

        graph.put_object(parent_object=self.page_config_id.page_id, connection_name="feed", message=self.message, link=self.link or None)

        post = graph.get_object(id=self.page_config_id.page_id, fields="posts{id,created_time}")
        # profile = graph.get_object(id ="me", fields="id,name,email")
        # for id in post['posts']

        post_ids_list = post['posts']['data']
        self.facebook_post_id = post_ids_list[0]['id']

        self.publish_date = datetime.now()
        print(self.publish_date)

        # print(datetime.strptime(post_ids_list[0]['created_time'], "%m %d %Y $H:%M:%S"))

        print(self.facebook_post_id)

        self.state = "publish"



    def test_date(self):
        time_r = "2019-06-19T07:49:40+0000".replace("T", " ")
        print(datetime.strptime(time_r, "%Y-%m-%d %H:%M:%S%z"))

        print(self.image)
        # print(datetime.strptime(post_ids_list[0]['created_time'], "%m %d %Y $H:%M:%S"))



    def fetch_comment(self):
        graph = facebook.GraphAPI(access_token=self.page_config_id.access_token,
                                  version=self.page_config_id.fb_api_version)
        posts_comment = graph.get_object(id=self.facebook_post_id, fields="comments")

        comment_data = posts_comment['comments']['data']

        fb_comment = self.env['fb.post.comment']

        for msg in comment_data:
            print(msg['created_time'])
            print(msg['id'])
            print(msg['message'])
            print(msg['from']['name'])
            print("==========")

            if not  self.comments_ids.filtered(lambda f: f.facebook_comment_id == msg['id']):
                fb_comment.create({
                    'post_id': self.id,
                    'create_by_fb_id' : msg['from']['id'],
                    "create_by" : msg['from']['name'],
                    "create_time" : msg['created_time'],
                    "comments" : msg['message'],
                    "facebook_comment_id" : msg['id'],
                })
            else:
                print("your Post is updated")

        print(comment_data,len(comment_data))





        # {'posts': {'paging': {'cursors': {
        #                 'before': 'Q2c4U1pXNTBYM0YxWlhKNVgzTjBiM0o1WDJsa',
        #                 'after': 'Q2c4U1pXNTBYM0YxWlhKNVgzTjBiM0o1WDJsa0'}},
        #
        #            'data': [{'id': '621082501727675_622063364962922'}, {'id': '621082501727675_622061158296476'},
        #                     {'id': '621082501727675_622053344963924'}, {'id': '621082501727675_622048801631045'},
        #                     {'id': '621082501727675_621908841645041'}, {'id': '621082501727675_621908354978423'},
        #                     {'id': '621082501727675_621906311645294'}, {'id': '621082501727675_621904528312139'},
        #                     {'id': '621082501727675_621886471647278'}, {'id': '621082501727675_621885351647390'}]},
        #  'id': '621082501727675'}
