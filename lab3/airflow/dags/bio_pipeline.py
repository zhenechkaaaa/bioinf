from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

BASE = "/mnt/c/Users/Evgenia/Documents/bioinf/lab3"

with DAG(
    dag_id="bio_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bioinformatics"],
) as dag:

    fastqc = BashOperator(
        task_id="fastqc",
        bash_command=f"""
        mkdir -p {BASE}/fastqc

        fastqc \
        {BASE}/data/SRR39039937_1.fastq \
        {BASE}/data/SRR39039937_2.fastq \
        -o {BASE}/fastqc
        """
    )

    mapping = BashOperator(
        task_id="mapping",
        bash_command=f"""
        bwa mem \
        {BASE}/reference/ecoli.fa \
        {BASE}/data/SRR39039937_1.fastq \
        {BASE}/data/SRR39039937_2.fastq \
        > {BASE}/alignment/sample.sam
        """
    )

    sam_to_bam = BashOperator(
        task_id="sam_to_bam",
        bash_command=f"""
        samtools view \
        -bS \
        {BASE}/alignment/sample.sam \
        > {BASE}/alignment/sample.bam
        """
    )

    flagstat = BashOperator(
        task_id="flagstat",
        bash_command=f"""
        samtools flagstat \
        {BASE}/alignment/sample.bam \
        > {BASE}/qc/flagstat.txt
        """
    )

    mapping_qc = BashOperator(
        task_id="mapping_qc",
        bash_command=f"""
        bash {BASE}/scripts/mapping_qc.sh \
        {BASE}/qc/flagstat.txt \
        > {BASE}/qc/qc_result.txt
        """
    )

    sort_bam = BashOperator(
        task_id="sort_bam",
        bash_command=f"""
        samtools sort \
        {BASE}/alignment/sample.bam \
        -o {BASE}/alignment/sample.sorted.bam
        """
    )

    index_bam = BashOperator(
        task_id="index_bam",
        bash_command=f"""
        samtools index \
        {BASE}/alignment/sample.sorted.bam
        """
    )

    freebayes = BashOperator(
        task_id="freebayes",
        bash_command=f"""
        freebayes \
        -f {BASE}/reference/ecoli.fa \
        {BASE}/alignment/sample.sorted.bam \
        > {BASE}/variants/sample.vcf
        """
    )

    fastqc >> mapping >> sam_to_bam

    sam_to_bam >> flagstat >> mapping_qc

    sam_to_bam >> sort_bam >> index_bam >> freebayes