package com.example.learning;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ComponentName;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void  sendMessage(View view){
        //响应按钮的事件
        EditText msg = findViewById(R.id.message);
        String s = msg.getText().toString();
        Log.i("message",s);

        //显式启动，写法一：class跳转
//        Intent intent = new Intent(this,SecondActivity.class);
//        this.startActivity(intent);

        //显式启动，写法二：包名.类名
//        Intent intent = new Intent();
//        intent.setClassName(this,"com.example.mainactivity.SecondActivity");
//        startActivity(intent);

        //显式启动，写法一：ComponentName
        Intent intent = new Intent();
        ComponentName cname = new ComponentName(this,MainActivity2.class);
        intent.setComponent(cname);
        startActivity(intent);
    }
}