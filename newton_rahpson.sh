export HADOOP_HOME=/opt/cloud/hadoop-0.20.2-cdh3u4
hadoop fs -rmr /fake_investments/out
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar\
    -input /fake_investments/in \
    -output /fake_investments/out \
    -mapper cat \
    -reducer nr_iterations_reducer.py \
    -file nr_iterations_reducer.py \
    -jobconf stream.num.map.output.key.fields=2 \
    -jobconf map.output.key.field.separator=\t \
    -jobconf num.key.fields.for.partition=1 \
