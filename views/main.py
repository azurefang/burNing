from views import BaseHandler
from config import POSTS_PAGINATION, REPLIES_PAGINATION
from models import *
from forms.main import *
from views import TornadoFormMultiDict


class IndexHandler(BaseHandler):
    def get(self):
        self.render('main/index.html')


class NodeHandler(BaseHandler):

    def get(self, node_name):
        form = PostForm()
        page = int(self.get_argument("page", 1))
        node = Node.select().where(Node.name==node_name)[0]
        posts = node.posts.paginate(page, POSTS_PAGINATION)
        current = datetime.now()
        self.render('main/node.html', posts=posts, form=form, current=current, node=node)

    def post(self, node_name):
        form = PostForm(TornadoFormMultiDict(self))
        if form.validate():
            post= Post(
                title=self.get_argument("title"),
                content=self.get_argument("content"),
                user = self.current_user(),
                node = Node.select().where(Node.name==node_name)[0]
            )
            post.save()
            self.redirect('/post/%s' % post.id)
        else:
            node = Node.select().where(Node.name==node_name)[0]
            current = datetime.now()
            posts = node.posts.paginate(1, POSTS_PAGINATION)
            self.render('/main/node.html', posts=posts, form=form, node=node, current=current)


class PostHandler(BaseHandler):
    def get(self, post_id):
        page = self.get_argument("page", 1)
        form = ReplyForm()
        post = Post.select().where(Post.id==post_id)[0]
        replies = post.replies.paginate(page, REPLIES_PAGINATION)
        self.render('main/post.html', post=post, replies=replies, form=form)

    def post(self, post_id):
        form = ReplyForm(TornadoFormMultiDict(self))
        post = Post.select().where(Post.id==post_id)[0]
        if form.validate():
            reply = Reply(
                content = self.get_argument("content"),
                user = self.current_user(),
                post = Post.select().where((Post.id==post_id))[0]
            )
            reply.save()
            post.last_reply_by = self.current_user()
            post.save()
            self.redirect('/post/%s' % post_id)
        else:
            replies = post.replies.paginate(1, REPLIES_PAGINATION)
            self.render('/main/post.html', post=post, replies=replies, form=form)



class ProfileHandler(BaseHandler):
    def get(self, username):
        user = User.select().where(username==username)[0]
        self.render('main/profile.html', user=user)
