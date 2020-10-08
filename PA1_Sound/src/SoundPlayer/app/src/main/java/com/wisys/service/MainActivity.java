package com.wisys.service;

import android.Manifest;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import com.wisys.service.R;

import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.media.MediaScannerConnection;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.os.IBinder;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    boolean isPlay = false;
    boolean isPause = false;

    //48K采样率
    int SamplingRate = 0;
    //时长5s
    int Duration = 15;
    //初始相位0
    double StartPlace = 0;
    //音量
    int Volume = 32766;

    //格式：双声道
    int channelConfiguration = AudioFormat.CHANNEL_IN_STEREO;
    //16Bit
    int audioEncoding = AudioFormat.ENCODING_PCM_16BIT;
    //是否在录制
    boolean isRecording = false;
    //每次从audiorecord输入流中获取到的buffer的大小
    int bufferSize = 0;
    int bufferSizeGenerate = 100;
    int frequency = 0;
    int frequencyDefault = 2000;
    String currentPath = "";
    String currentURI = "";
    TextView the_textview;
    EditText the_frequency;
    EditText the_sample;
    Button StartRecord, StopRecord, ChooseButton, GenerateButton;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        the_textview = findViewById(R.id.show);
        StartRecord = findViewById(R.id.record_self);
        StopRecord = findViewById(R.id.record_end);
        ChooseButton = findViewById(R.id.select_local);
        the_frequency = findViewById(R.id.frequency);
        the_sample = findViewById(R.id.sample);
        GenerateButton = findViewById(R.id.generate);
        GetPermission();

        //完成每个按钮的功能
        StartRecord.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    String f = the_sample.getText().toString();
                    SamplingRate = Integer.parseInt(f);
                    if (SamplingRate <= 0) {
                        Exception e = new Exception();
                        throw (e);
                    }
                    //恢复停止录音按钮，并禁用开始录音按钮
                    StopRecord.setEnabled(true);
                    StartRecord.setEnabled(false);
                    Thread thread = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            //设置用于临时保存录音原始数据的文件的名字
                            String name = Environment.getExternalStorageDirectory().getAbsolutePath() + "/raw.wav";
                            //调用开始录音函数，并把原始数据保存在指定的文件中
                            StartRecord(name);
                            //获取此刻的时间
                            Date now = Calendar.getInstance().getTime();
                            //用此刻时间为最终的录音wav文件命名
                            String filepath = Environment.getExternalStorageDirectory().getAbsolutePath() + "/record_" + now.toString() + ".wav";
                            scanFile(getApplicationContext(), filepath);

                            //把录到的原始数据写入到wav文件中。
                            copyWaveFile(name, filepath);
                        }
                    });
                    //开启线程
                    thread.start();
                }
                catch(Exception e)
                {
                    Toast tt = Toast.makeText(getApplicationContext(), "录音失败！", Toast.LENGTH_LONG);
                    tt.show();
                }
            }

        });

        StopRecord.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //停止录音
                isRecording = false;
                //恢复开始录音按钮，并禁用停止录音按钮
                StopRecord.setEnabled(false);
                StartRecord.setEnabled(true);
            }
        });

        ChooseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("audio/*");
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                startActivityForResult(intent, 0);
            }
        });
    }

    /**播放器控制函数**/
    // TODO Method to start the service
    public void startPlayer(View view) {
        isPlay = true;
        Intent intent = new Intent(this, MusicService.class);
        intent.putExtra("key", "play");
        intent.putExtra("url", currentURI);
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

    //打开本地文件
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // TODO Auto-generated method stub
        try {
            if (resultCode == Activity.RESULT_OK) {
                Uri uri = data.getData();
                currentURI = uri.toString();
                Cursor cur = getContentResolver().query(uri,
                        null,
                        null, null, null);
                int place_path = cur.getColumnIndexOrThrow(MediaStore.Audio.Media.DISPLAY_NAME);
                cur.moveToFirst();
                currentPath = cur.getString(place_path);
                the_textview.setText("当前播放音频位置： " + currentPath);
                cur.close();
            }
        } catch (Throwable t) {
            currentURI = "";
            currentPath = "";
            Toast tt = Toast.makeText(this, "读取本地文件失败！", Toast.LENGTH_LONG);
            tt.show();

        }
    }



    /**录音函数**/
    //通知媒体库更新文件
    public void scanFile(Context context, String filePath) {
        Intent scanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        scanIntent.setData(Uri.fromFile(new File(filePath)));
        context.sendBroadcast(scanIntent);
    }

    private void GetPermission() {

        /*在此处插入运行时权限获取的代码*/
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)!=
                PackageManager.PERMISSION_GRANTED||
                ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)!=
                        PackageManager.PERMISSION_GRANTED||
                ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)!=
                        PackageManager.PERMISSION_GRANTED
        )
        {
            ActivityCompat.requestPermissions(this,
                    new String[]{android.Manifest.permission.RECORD_AUDIO,
                            android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
                            Manifest.permission.READ_EXTERNAL_STORAGE}, 0);
        }
    }

    //开始录音
    public void StartRecord(String name) {

        //生成原始数据文件
        File file = new File(name);
        //如果文件已经存在，就先删除再创建
        if (file.exists())
            file.delete();
        try {
            file.createNewFile();
        } catch (IOException e) {
            throw new IllegalStateException("未能创建" + file.toString());
        }
        try {
            //文件输出流
            OutputStream os = new FileOutputStream(file);
            BufferedOutputStream bos = new BufferedOutputStream(os);
            DataOutputStream dos = new DataOutputStream(bos);
            //获取在当前采样和信道参数下，每次读取到的数据buffer的大小
            bufferSize = AudioRecord.getMinBufferSize(SamplingRate, channelConfiguration, audioEncoding);
            //建立audioRecord实例
            AudioRecord audioRecord = new AudioRecord(MediaRecorder.AudioSource.MIC, SamplingRate, channelConfiguration, audioEncoding, bufferSize);

            //设置用来承接从audiorecord实例中获取的原始数据的数组
            byte[] buffer = new byte[bufferSize];
            //启动audioRecord
            audioRecord.startRecording();
            //设置正在录音的参数isRecording为true
            isRecording = true;
            //只要isRecording为true就一直从audioRecord读出数据，并写入文件输出流。
            //当停止按钮被按下，isRecording会变为false，循环停止
            while (isRecording) {
                int bufferReadResult = audioRecord.read(buffer, 0, bufferSize);
                for (int i = 0; i < bufferReadResult; i++) {
                    dos.write(buffer[i]);
                }
            }
            //停止audioRecord，关闭输出流
            audioRecord.stop();
            dos.close();
        } catch (Throwable t) {
            Toast tt = Toast.makeText(this, "录音失败！", Toast.LENGTH_LONG);
            tt.show();
        }
    }

    //复制录音文件
    private void copyWaveFile(String inFileName, String outFileName)
    {
        FileInputStream in = null;
        FileOutputStream out = null;
        long totalAudioLen = 0;
        //wav文件比原始数据文件多出了44个字节，除去表头和文件大小的8个字节剩余文件长度比原始数据多36个字节
        long totalDataLen = totalAudioLen + 36;
        long longSampleRate = SamplingRate;
        int channels = 2;
        //每分钟录到的数据的字节数
        long byteRate = 16 * SamplingRate * channels / 8;

        byte[] data = new byte[bufferSize];
        try
        {
            in = new FileInputStream(inFileName);
            out = new FileOutputStream(outFileName);
            //获取真实的原始数据长度
            totalAudioLen = in.getChannel().size();
            totalDataLen = totalAudioLen + 36;
            //为wav文件写文件头
            WriteWaveFileHeader(out, totalAudioLen, totalDataLen, longSampleRate, channels, byteRate);
            //把原始数据写入到wav文件中。
            while(in.read(data) != -1)
            {
                out.write(data);
            }
            in.close();
            out.close();
        } catch (FileNotFoundException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }


    //音频文件头
    private void WriteWaveFileHeader(FileOutputStream out, long totalAudioLen,
                                     long totalDataLen, long longSampleRate, int channels, long byteRate)
            throws IOException {
        byte[] header = new byte[44];
        header[0] = 'R'; // RIFF/WAVE header
        header[1] = 'I';
        header[2] = 'F';
        header[3] = 'F';
        header[4] = (byte) (totalDataLen & 0xff);
        header[5] = (byte) ((totalDataLen >> 8) & 0xff);
        header[6] = (byte) ((totalDataLen >> 16) & 0xff);
        header[7] = (byte) ((totalDataLen >> 24) & 0xff);
        header[8] = 'W';
        header[9] = 'A';
        header[10] = 'V';
        header[11] = 'E';
        header[12] = 'f'; // 'fmt ' chunk
        header[13] = 'm';
        header[14] = 't';
        header[15] = ' ';
        header[16] = 16;
        header[17] = 0;
        header[18] = 0;
        header[19] = 0;
        header[20] = 1; // WAV type format = 1
        header[21] = 0;
        header[22] = (byte) channels; //指示是单声道还是双声道
        header[23] = 0;
        header[24] = (byte) (longSampleRate & 0xff); //采样频率
        header[25] = (byte) ((longSampleRate >> 8) & 0xff);
        header[26] = (byte) ((longSampleRate >> 16) & 0xff);
        header[27] = (byte) ((longSampleRate >> 24) & 0xff);
        header[28] = (byte) (byteRate & 0xff); //每分钟录到的字节数
        header[29] = (byte) ((byteRate >> 8) & 0xff);
        header[30] = (byte) ((byteRate >> 16) & 0xff);
        header[31] = (byte) ((byteRate >> 24) & 0xff);
        header[32] = (byte) (2 * 16 / 8); // block align
        header[33] = 0;
        header[34] = 16; // bits per sample
        header[35] = 0;
        header[36] = 'd';
        header[37] = 'a';
        header[38] = 't';
        header[39] = 'a';
        header[40] = (byte) (totalAudioLen & 0xff); //真实数据的长度
        header[41] = (byte) ((totalAudioLen >> 8) & 0xff);
        header[42] = (byte) ((totalAudioLen >> 16) & 0xff);
        header[43] = (byte) ((totalAudioLen >> 24) & 0xff);
        //把header写入wav文件
        out.write(header, 0, 44);
    }











    public static byte[] ShortToBytes(short values, ByteOrder byteOrder) {
        byte[] buffer = new byte[2];
        for (int i = 0; i < 2; i++) {
            int intVal = (int) values;
            byte lowByte = (byte)(intVal & 0xff);
            int paf = 0x00;
            if(intVal < 0) paf = 0x80;
            int pad = ((intVal >>> 7) & 0x7f);
            byte highByte = (byte)(paf | pad);
            if(byteOrder == ByteOrder.BIG_ENDIAN){
                buffer[0] = highByte;
                buffer[1] = lowByte;
            }else{
                buffer[0] = lowByte;
                buffer[1] = highByte;
            }
        }
        return buffer;
    }


    public void GenerateAudio(View view)
    {
        try {
            String f = the_frequency.getText().toString();
            frequency = Integer.parseInt(f);
            if (frequency <= 0) {
                Exception e = new Exception();
                throw (e);
            }
            String ff = the_sample.getText().toString();
            SamplingRate = Integer.parseInt(ff);
            if (SamplingRate <= 0) {
                Exception e = new Exception();
                throw (e);
            }


            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    //设置用于临时保存录音原始数据的文件的名字
                    String name = Environment.getExternalStorageDirectory().getAbsolutePath() + "/raw_generate.wav";
                    //调用开始录音函数，并把原始数据保存在指定的文件中
                    GenerateWave(name, frequency);
                    //获取此刻的时间
                    Date now = Calendar.getInstance().getTime();
                    //用此刻时间为最终的录音wav文件命名
                    String filepath = Environment.getExternalStorageDirectory().getAbsolutePath() + "/generate_" + now.toString() + ".wav";
                    //把录到的原始数据写入到wav文件中。
                    copyWaveFileGenerate(name, filepath);
                    scanFile(getApplicationContext(), filepath);
                }
            });
            //开启线程
            thread.start();
        }
        catch(Exception e)
        {
            Toast tt = Toast.makeText(this, "频率不合法,需要是正整数！", Toast.LENGTH_LONG);
            tt.show();

        }
    }

    //生成波
    public void GenerateWave(String name, int frequency) {

        //生成原始数据文件
        File file = new File(name);
        //如果文件已经存在，就先删除再创建
        if (file.exists())
            file.delete();
        try {
            file.createNewFile();
        } catch (IOException e) {
            throw new IllegalStateException("未能创建" + file.toString());
        }
        try {
            //文件输出流
            OutputStream os = new FileOutputStream(file);
            BufferedOutputStream bos = new BufferedOutputStream(os);
            DataOutputStream dos = new DataOutputStream(bos);


            //设置用来承接从audiorecord实例中获取的原始数据的数组
            byte[] buffer = makeSound(SamplingRate, Duration, frequency, StartPlace, Volume);
            //写文件
            for (int i = 0; i < SamplingRate * Duration * 2; i++) {
                dos.write(buffer[i]);
            }

            dos.close();
        } catch (Throwable t) {
            Log.e("MainActivity", "生成音频失败");
        }
    }

    /**
     * 产生余弦波
     * 直接用三角函数做循环计算，并把算出的结果转为Byte数组
     */
    private byte[] makeSound(int framerate, int duration, int frequency, double start_place, int volume)
    {
        byte[] result = new byte[framerate * duration * 8];
        int num = framerate * duration;
        for(int i = 0; i < num; i ++)
        {
            double place = 2 * Math.PI * Double.valueOf(frequency) * Double.valueOf(i) / Double.valueOf(framerate) + start_place;
            short y = (short) Math.round(Math.sin(place) * volume);
            byte[] byte_y = ShortToBytes(y, ByteOrder.nativeOrder());
            for(int j = 0; j < 2; j ++)
            {
                result[i * 2 + j] = byte_y[j];
            }
        }
        return result;
    }

    //复制波形代码
    private void copyWaveFileGenerate(String inFileName, String outFileName)
    {
        FileInputStream in = null;
        FileOutputStream out = null;
        long totalAudioLen = 0;
        //wav文件比原始数据文件多出了44个字节，除去表头和文件大小的8个字节剩余文件长度比原始数据多36个字节
        long totalDataLen = totalAudioLen + 36;
        long longSampleRate = SamplingRate;
        int channels = 1;
        //每分钟录到的数据的字节数
        long byteRate = 16 * SamplingRate * channels / 8;

        byte[] data = new byte[bufferSizeGenerate];
        try
        {
            in = new FileInputStream(inFileName);
            out = new FileOutputStream(outFileName);
            //获取真实的原始数据长度
            totalAudioLen = in.getChannel().size();
            totalDataLen = totalAudioLen + 36;
            //为wav文件写文件头
            WriteWaveFileHeader(out, totalAudioLen, totalDataLen, longSampleRate, channels, byteRate);
            //把原始数据写入到wav文件中。
            while(in.read(data) != -1)
            {
                out.write(data);
            }
            in.close();
            out.close();

        } catch (FileNotFoundException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
