#!/usr/bin/env pwsh

$input_dir = $args[0]
$output_dir = $args[1]
$optional_1 = $args[2]
$optional_2 = $args[3]
$optional_3 = $args[4]
$optional_4 = $args[5]

If ( $null -eq $input_dir)
{
  Write-Error -Message "Error! Input directory not set" -Category NotSpecified -RecommendedAction "Set a path to the input directory"
  exit 1
}

ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Error! Input directory not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $output_dir)
{
  Write-Error -Message "Error! Output directory not set" -Category NotSpecified -RecommendedAction "Set a path t the output directory"
  exit 1
}

ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory not found" -Category ObjectNotFound
  exit 1
}

python -m pipeline.train --input $input_dir --output $output_dir $optional_1 $optional_2 $optional_3 $optional_4
