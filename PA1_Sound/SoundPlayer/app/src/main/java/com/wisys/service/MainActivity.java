package com.wisys.service;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import com.wisys.service.R;
import android.content.ServiceConnection;
import android.database.Cursor;
import android.net.Uri;
import android.os.IBinder;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    boolean isPlay = false;
    boolean isPause = false;
    String currentTitle = "";
    String currentPath = "";
    TextView the_textview;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        the_textview = findViewById(R.id.show);
    }

    public void selectAudio(View view) {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("audio/x-wav");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(intent, 0);
    }

    //TODO
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // TODO Auto-generated method stub
        super.onActivityResult(requestCode, resultCode, data);
        Uri uri = data.getData();

        Cursor cur = getContentResolver().query(uri,
                new String[]{MediaStore.Audio.Media.DATA},        //音频文件路径
                null, null, null);
        int place_path = cur.getColumnIndexOrThrow(MediaStore.Audio.Media.DATA);
        cur.moveToFirst();
        currentPath = cur.getString(place_path);
        the_textview.setText("当前播放音频位置： " + currentPath);
    }



    // TODO Method to start the service
    public void startPlayer(View view) {
        isPlay = true;
        Intent intent = new Intent(this, MusicService.class);
        intent.putExtra("key", "play");
        intent.putExtra("url", currentPath);
        startService(intent);
    }
    public void stopPlayer(View view) {
        if(isPlay = true) {
            isPlay = false;
            Intent intent = new Intent(this, MusicService.class);
            intent.putExtra("key", "stop");
            startService(intent);
        }
    }

    // TODO Method to pause the service
    public void pausePlayer(View view) {
        if(isPlay == true && isPause == false)
        {
            isPause = true;
            Intent intent = new Intent(this, MusicService.class);
            intent.putExtra("key", "pause");
            startService(intent);
        }


    }

    public void resumePlayer(View view) {
        if(isPlay == true && isPause == true)
        {
            isPause = false;
            Intent intent = new Intent(this, MusicService.class);
            intent.putExtra("key", "resume");
            startService(intent);
        }
    }

}
