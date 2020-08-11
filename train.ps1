#!/usr/bin/env pwsh

$input_dir = $args[0]
$output_dir = $args[1]
$optional_1 = $args[2]
$optional_2 = $args[3]
$optional_3 = $args[4]
$optional_4 = $args[5]

If ( $input_dir -eq $null )
{
  Write-Host "Error! Input directory not set" -ForegroundColor Red
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Host "Error! Input directory not found" -ForegroundColor Red
  exit 1
}


If ( $output_dir -eq $null )
{
  Write-Host "Error! Output directory not set" -ForegroundColor Red
  exit 1
}


python -m pipeline.train --input $input_dir --output $output_dir $optional_1 $optional_2 $optional_3 $optional_4
