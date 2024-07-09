# usr/bin/env python
# -*- coding:utf-8- -*-
from django import forms
from login.models import student, teacher,course,SC


class StuLoginForm(forms.Form):
    sno = forms.CharField(label='学号', max_length=10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)


class TeaLoginForm(forms.Form):
    tno = forms.CharField(label='教职工号', max_length=10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)


class StuRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = student
        fields = ('sgrade',
                  'sname',
                  'spasswd',
                  'confirm_password',
                  'ssex',
                  'sbirthdate',
                  'scollege',
                  'smajor')

    def clean(self):
        cleaned_data = super(StuRegisterForm, self).clean()
        password = cleaned_data.get('spasswd')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', '两次密码输入不一致！')

        return cleaned_data


'''
class StuUpdateForm(StuRegisterForm):
    class Meta:
        model = student
        fields = ('name',
                  'password',
                  'confirm_password',
                  'gender',
                  'birthday',
                  'email',
                  'info')
'''

class TeaRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = teacher
        fields = ('tname',
                  'tpasswd',
                  'confirm_password',
                  'tsex',
                  'tbirthdate',
                  'tcollege')

    def clean(self):
        cleaned_data = super(TeaRegisterForm, self).clean()
        password = cleaned_data.get('tpasswd')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', '两次密码输入不一致！')



class createCourse(forms.ModelForm):
    class Meta:
        model=course
        fields = ('cname',
                 'ccredit',
                 'pcno'
        )

    def clean(self):
        cleaned_data=super(createCourse,self).clean()
        pcno=cleaned_data.get('pcno')
        if pcno:
            pcno_set = course.objects.filter(cno=pcno)
            if pcno_set.count() == 0:
                self.add_error('pcno', '该先修课程不存在！')


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='原密码', widget=forms.PasswordInput)
    new_password = forms.CharField(label='新密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            self.add_error('confirm_password',"两次密码输入不一致！")
