package com.wisys.service;

import android.app.Service;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Binder;
import android.os.IBinder;

import java.io.IOException;

public class MusicService extends Service {

    //media player
    private MediaPlayer mediaPlayer;
    //Used to pause/resume MediaPlayer
    private int resumePosition;

    private MusicBinder mBinder = new MusicBinder();

    public class MusicBinder extends Binder {
        MusicService getService() {
            return MusicService.this;
        }
    }


    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        return super.onUnbind(intent);
    }

    public int onStartCommand(Intent intent, int flags, int startId) {
        String Message = intent.getStringExtra("key");
        System.out.println(Message);
        if(Message.equals("play"))
        {
            String url = intent.getStringExtra("url");
            playMedia(url);
        }
        else if(Message.equals("stop"))
        {
            stopMedia();
        }
        else if(Message.equals("pause"))
        {
            pauseMedia();
        }
        else if(Message.equals("resume"))
        {
            resumeMedia();
        }
        return super.onStartCommand(intent, flags, startId);


    }

    @Override
    public void onCreate(){
        super.onCreate();
        //create player
        mediaPlayer = MediaPlayer.create(this, R.raw.rainbow);
    }

    @Override

    public void onDestroy() {
        super.onDestroy();
        //先停止 再释放
        if(mediaPlayer != null) {
            if (mediaPlayer.isPlaying()) {
                mediaPlayer.stop();
            }
            mediaPlayer.release();
        }
    }

    private void playMedia(String url) {
        if(mediaPlayer != null) {
            resumePosition = 0;
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
        Uri playUri = Uri.parse(url);
        mediaPlayer = MediaPlayer.create(this, playUri);
        mediaPlayer.start();
    }

    private void stopMedia() {
        if(mediaPlayer != null) {
            resumePosition = 0;
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    private void pauseMedia() {
        if(mediaPlayer != null && mediaPlayer.isPlaying()) {

            mediaPlayer.pause();
            resumePosition = mediaPlayer.getCurrentPosition();
        }
    }

    private void resumeMedia() {
        if(mediaPlayer != null && !mediaPlayer.isPlaying()) {

            mediaPlayer.seekTo(resumePosition);
            mediaPlayer.start();
        }
    }

}
