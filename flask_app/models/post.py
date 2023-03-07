from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = data['name']
        self.user_alias=data['alias']
        self.likes=data['count(l.id)']


    @staticmethod
    def validate(post):
        is_valid = True  
        if len(post['post']) < 1:
            flash("Post must be at least 1 character in length.")
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts ( content, created_at, updated_at, user_id) VALUES ( %(content)s, NOW() , NOW(), %(user_id)s );"
        
        return connectToMySQL('indiv_proj').query_db(query, data)

 
    @classmethod
    def get_all(cls):
        query = "select u.alias, u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id, count(l.id) from posts as p left join users as u on user_id=u.id left join likes as l on p.id=l.post_id group by  u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id"
        
        results = connectToMySQL('indiv_proj').query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts
    
    @classmethod
    def get_one(cls,data):
        query = "select u.alias, u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id, count(l.id) from posts as p left join users as u on user_id=u.id left join likes as l on p.id=l.post_id where p.id=%(post_id)s group by u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id"
        
        results = connectToMySQL('indiv_proj').query_db(query,data)
        posts = results
        return posts
    # @classmethod
    # def get_one(cls,data):
    #     query = "select u.alias, u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id, count(l.id) from posts as p left join users as u on user_id=u.id left join likes as l on p.id=l.post_id where p.id=%(post_id)s group by u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id"
        
    #     results = connectToMySQL('indiv_proj').query_db(query,data)
    #     posts = []
    #     for post in results:
    #         posts.append(cls(post))
    #     return posts
    
    # @classmethod
    # def delete(cls,data):
    #     try:
    #         connectToMySQL('indiv_proj').query_db('delete from likes where post_id=%(post_id)s;',data)
    #         query = "delete from posts where id=%(post_id)s;"
    #         return connectToMySQL('indiv_proj').query_db(query, data)
    #     except:
    #         query = "delete from posts where id=%(post_id)s;"
    #         return connectToMySQL('indiv_proj').query_db(query, data)
        
    @classmethod
    def delete(cls,data):
        if 'user_id' in session:
            check = connectToMySQL('indiv_proj').query_db('select user_id from posts where id=%(post_id)s;',data)
            print(check[0]['user_id'])
            print(session['user_id'])
            if session['user_id'] == check[0]['user_id']:
                try:
                    connectToMySQL('indiv_proj').query_db('delete from likes where post_id=%(post_id)s;',data)
                    query = "delete from posts where id=%(post_id)s;"
                    return connectToMySQL('indiv_proj').query_db(query, data)
                except:
                    query = "delete from posts where id=%(post_id)s;"
                    return connectToMySQL('indiv_proj').query_db(query, data)
            else:
                print('DONT OWN IT')
                return 0
        print('NOT LOGGED')
        return 0
    
    @classmethod
    def get_likes(cls, data):
        query = "select distinct u.alias, u.name, u.last_name from likes as l left join users as u on user_id=u.id where post_id=%(post_id)s;"
        result = connectToMySQL("indiv_proj").query_db(query, data)
        
        if len(result) < 1:
            return False
        return result