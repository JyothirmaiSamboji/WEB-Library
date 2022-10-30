import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Subjects(db.Model):
    __tablename__="Subjects"
    subID = db.Column(db.Integer, primary_key=True)
    subName =db.Column(db.String,nullable=False)
    
class usersList(db.Model):
    __tablename__="users"
    userID=db.Column(db.Integer, primary_key=True)
    userName=db.Column(db.String,nullable=False)  
    password=db.Column(db.String,nullable=False)  
    userType=db.Column(db.String,nullable=False) 
  
class bookMaster(db.Model):
    __tablename__="bookMaster"
    accNumber = db.Column(db.String, primary_key=True)
    bookTitle = db.Column(db.String,nullable=False)
    SubID = db.Column(db.Integer,db.ForeignKey("Subjects.subID"), nullable=False)
    authorName = db.Column(db.String,nullable=False)
    PublisherName = db.Column(db.String,nullable=False)
    pages = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String,nullable=False)
    subject = db.relationship("Subjects", backref="subject", lazy=True)
  
class IssueReturn(db.Model):
    __tablename__="IssueReturn"
    transID=db.Column(db.Integer, primary_key=True)
    AccNumber = db.Column(db.String,db.ForeignKey("bookMaster.accNumber"), nullable=False)
    userID=db.Column(db.Integer,db.ForeignKey("users.userID"), nullable=False)
    IssueDate = db.Column(db.Date, nullable=False)
    ExpRetDate = db.Column(db.Date,nullable=False)
    ActRetDate = db.Column(db.Date,nullable=False)
    OverdueDays = db.Column(db.Integer,nullable=False)
    book = db.relationship("bookMaster", backref="book", lazy=True)
    usr = db.relationship("usersList", backref="user", lazy=True)
   